from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class ItemDataManager(models.Manager):
    def add_dict_item(self, dict):
        print(dict)
        try:
            itemdata = self.create(user=dict['user'], title=dict['title'], domeme_id=int(dict['domeme_id']),
                                   domeme_price=float(dict['domeme_price']), naver_id=int(dict['naver_id']), 
                                   naver_price=float(dict['naver_price']), naver_sale=float(dict['naver_sale']),
                                   naver_discounted_price=(float(dict['naver_price'])-float(dict['naver_sale'])),
                                   margin_ratio=((1-(float(dict['domeme_price'])/(float(dict['naver_price'])-float(dict['naver_sale']))))*100),
                                   create_date=timezone.now())
        except:
            print("create 실패 domeme:"+str(dict['domeme_id'])+" naver:"+str(dict['naver_id']))
            itemdata = None
        return itemdata

class TitleReplace(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    before = models.CharField(max_length=255)
    after = models.CharField(max_length=255, blank=True, default=" ")
    priority = models.IntegerField(default=5)

    def __str__(self):
        return "["+str(self.priority)+"] '"+self.before+"' -> '"+self.after+"'"

class ItemData(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    domeme_id = models.IntegerField(unique=True)
    domeme_price = models.FloatField(null=True, default=0)
    domeme_row_price = models.FloatField(null=True, default=-1)
    domeme_update_count = models.IntegerField(default=0)

    naver_id = models.IntegerField(unique=True)
    naver_edit_id = models.IntegerField(default=-1)
    naver_price = models.FloatField()
    naver_sale = models.FloatField()
    naver_discounted_price = models.FloatField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(default=timezone.now)
    category_current = models.CharField(max_length=255, default='')
    category_score = models.IntegerField(default=99999)
    category_recommand = models.CharField(max_length=255, default='')

    detail_page = models.IntegerField(default=-1)
    search_tag = models.CharField(max_length=1024, default='')
    search_tag_list = models.CharField(max_length=2048, default='')

    price_state = models.IntegerField(default=0)
    margin_ratio = models.FloatField(default=0.0)

    minimum_count = models.IntegerField(default=1)

    objects = ItemDataManager()

    def set_item_info(self, item_info):
        if item_info:
            if 'naver_id' in item_info and int(item_info['naver_id']) > 0 and self.naver_id != int(item_info['naver_id']):
                print("네이버 아이디 업데이트 : "+str(item_info['naver_id'])+" -> "+str(item_info['naver_id']))
                self.naver_id = int(item_info['naver_id'])
            if 'category_score' in item_info and item_info['category_score']:
                print("카테고리 정보 업데이트 : "+str(item_info['category_score'])+" ** "+str(item_info['category_recommand']))
                self.category_score = int(item_info['category_score'])
                self.category_recommand = item_info['category_recommand']
            if 'category_current' in item_info and item_info['category_current']:
                self.category_current = item_info['category_current']
            if self.naver_edit_id == -1 and int(item_info['naver_edit_id']) != -1:
                print("네이버 에딧 아이디 업데이트 : "+str(self.naver_edit_id)+" -> "+str(item_info['naver_edit_id']))
                self.naver_edit_id = int(item_info['naver_edit_id'])
            if self.title != item_info['title']:
                print("네이버 상품명 업데이트 : "+self.title+" -> "+str(item_info['title']))
                self.title = item_info['title']
            print("아이템 데이터 저장")
            self.modify_date = timezone.now()
            self.save()
        else:
            print("빈 오브젝트 입력으로 데이터 삭제")
            self.delete()

    def set_domeme_price(self, domeme_price, domeme_row_price):
        self.price_state = 0
        if self.domeme_price > 0 and self.domeme_price < domeme_price:
            print("도매매 가격 상향 "+str(self.domeme_price)+" -> "+str(domeme_price))
            self.price_state = 1
            self.domeme_update_count = self.domeme_update_count + 1
        self.domeme_price = domeme_price
        if domeme_row_price > 0:
            self.domeme_row_price = domeme_row_price
        elif self.naver_sale == 0:
            self.price_state = 4            
        if self.naver_discounted_price < self.domeme_price * 1.15:
            print("도매매 가격대비 쌈 "+str(self.naver_discounted_price)+" -> "+str(self.domeme_price * 1.15))
            self.price_state = 2
        if self.naver_discounted_price < self.domeme_row_price:
            print("권장 최저가보다 쌈")
            self.price_state = 3

    def set_margin_ratio(self):
        self.naver_discounted_price = self.naver_price - self.naver_sale
        self.margin_ratio = ((1 - (self.domeme_price * self.minimum_count / self.naver_discounted_price))*100)

    def update_with_naver_info(self, naver_info):
        if not self.title == naver_info['title']:
            self.title = naver_info['title']
        if not self.naver_price == float(naver_info['naver_price']):
            self.naver_price = float(naver_info['naver_price'])
        if naver_info['naver_sale'] == '-':
            naver_info['naver_sale'] = 0.0
        if not self.naver_sale == float(naver_info['naver_sale']):
            self.naver_sale = float(naver_info['naver_sale'])
        self.set_margin_ratio()

    def update_naver_price_from_info(self, naver_info):
        self.naver_price = float(naver_info['naver_price'])
        if naver_info['naver_sale'] == "-":
            self.naver_sale = 0
        else:
            self.naver_sale = float(naver_info['naver_sale'])
        self.set_margin_ratio()
        print("네이버 현재 저장된 가격 갱신: "+str(self.naver_price)+" - "+str(self.naver_sale))

    def update_naver_price(self, naver_price, naver_sale):
        print("네이버 가격 업데이트")
        self.naver_price = naver_price
        self.naver_sale = naver_sale
        self.price_state = 0
        self.set_margin_ratio()
        self.modify_date = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        self.modify_date = timezone.now()
        super(ItemData, self).save(*args, **kwargs)

