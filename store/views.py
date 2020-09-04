from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import ItemData, TitleReplace
from .domeme_parser import Domeme
from .naver_parser import Naver
from .scout_parser import Scout

# Create your views here.

# 세션에서 네이버 창과 도매매 창을 유지하려고 해보았으나, 세션을 저장하는 함수에서 json으로 시리얼라이즈를 하는데,
# 해당 작업에서 selenium 객체들을 시리얼라이즈하는데 실패함 serialize관련 내용을 추가하던가 해야할듯
# def get_domeme(request):
#     domeme = request.session.get('domeme')
#     if not domeme:
#         request.session['domeme'] = Domeme()
#         domeme = request.session['domeme']
#     return domeme

# def get_naver(request):
#     naver = request.session.get('naver')
#     if not naver:
#         request.session['naver'] = Naver()
#         naver = request.session['naver']
#     return naver

def get_domeme(request):
    return Domeme()

def get_naver(request):
    return Naver()

def get_index_dict(request, item_list):
    unset_sale_count = ItemData.objects.filter(user=request.user, naver_sale=0, domeme_row_price=-1).count()
    uncorrect_upper_margin = ItemData.objects.filter(user=request.user, margin_ratio__gt=25).order_by('-margin_ratio')
    unset_naver_edit_id = ItemData.objects.filter(user=request.user, naver_edit_id=-1)
    soldout_list = []
    return {'soldout_list':soldout_list, 'unset_sale_count':unset_sale_count, 'uncorrect_upper_margin':uncorrect_upper_margin, 'unset_naver_edit_id':unset_naver_edit_id, 'item_list':item_list}

def index_view(request):
    item_list = ItemData.objects.filter(user=request.user).order_by('margin_ratio')
    return_dict = get_index_dict(request, item_list)
    return render(request, 'store/itemdata_list.html', return_dict)

def index_order_by_category_score(request):
    item_list = ItemData.objects.filter(user=request.user).order_by('-category_score')
    return_dict = get_index_dict(request, item_list)
    return render(request, 'store/itemdata_list.html', return_dict)

def reset_category_score(request):
    item_list = ItemData.objects.filter(user=request.user)
    for item in item_list:
        item.category_score = 99999
        item.save()

def detail_view(request, pk):
    return render(request, 'store/itemdata_detail.html')

class ItemDataDetailView(generic.DetailView):
    model = ItemData
        
def soldout_view(request, pk):
    return render(request, 'store/soldout_list.html')

def clear_soldout(request):
    domeme = get_domeme(request)
    domeme.clear_soldout()
    return redirect(reverse('store:index'))

def create_item(request):
    return redirect(reverse('store:index'))

''' 네이버에는 등록되었으나, 서버 디비에는 등록되지 않은 데이터를 가져온다. '''
def load_naver_data(request, load_count=0):
    item_list = ItemData.objects.filter(user=request.user)
    except_list = []
    for item in item_list:
        except_list.append(item.domeme_id)

    domeme = get_domeme(request)
    naver = get_naver(request)
    naver_item_list = naver.get_sale_unset_item_list(except_list, depth=1, load_count=load_count)
    count = 0
    for naver_item in naver_item_list:
        process_print(count, len(naver_item_list))
        naver_item['user'] = request.user
        if naver_item['naver_sale'] == "-":
            naver_item['naver_sale'] = 0
        naver_item['title'] = title_replace(request.user, naver_item['title'])
        item = ItemData.objects.add_dict_item(naver_item)

        refresh_item(request, domeme, naver, item, depth=1)
        count = count + 1
    return redirect(reverse('store:index'))

def load_domeme_data(request):
    domeme = get_domeme(request)
    naver = get_naver(request)
    item_list = ItemData.objects.filter(user=request.user).order_by('-domeme_update_count', 'modify_date')
    
    count = 0
    start_time = timezone.now()
    for item in item_list:
        domeme_info = domeme.get_item_info(item.domeme_id)
        process_print(count, len(item_list))
        print("업데이트 카운트: "+str(item.domeme_update_count)+" 수정일자: "+str(item.modify_date))
        if domeme_info:
            item.set_domeme_price(float(domeme_info['domeme_price']), float(domeme_info['domeme_row_price']))
            # if item.naver_edit_id == -1:
            #     item.naver_edit_id = naver.get_edit_id(item.naver_id)
            #     if item.naver_edit_id == -1:
            #         print("네이버에서 제거됨으로 인한 "+str(item.domeme_id)+" 물건 제거")
            #         item.delete()
            #         continue
            #     else:
            #         print("네이버 에딧 아이디 업데이트: "+str(item.naver_id)+" => "+str(item.naver_edit_id))
            if item.price_state > 0:
                item_dict = vars(item)
                (naver_price, naver_sale) = naver.set_price(item_dict, goto_page=True, depth=1)
                if naver_price and naver_sale:
                    print("변경된 네이버 가격: "+str(naver_price)+" - "+str(naver_sale))
                    item.update_naver_price(naver_price, naver_sale)
                else:
                    print("네이버에서 제거됨으로 인한 "+str(item.domeme_id)+" 물건 제거")
                    item.delete()
                    continue
            item.save()
        else:
            print(str(item.domeme_id)+" 물건 제거")
            item.delete()
        count = count + 1
        end_time = timezone.now()
        delta = end_time - start_time
        average_time = delta.total_seconds() / count
        print("건당 평균 시간: "+format(average_time, ".2f")+"초 전체 시간:"+format(delta.total_seconds(), ".2f")+"초")

    end_time = timezone.now()
    delta = end_time - start_time
    print("총 걸린 시간: "+format(delta.total_seconds(), ".2f")+"초")
    return redirect(reverse('store:index'))

def load_naver_price(request):
    item_list = ItemData.objects.filter(user=request.user).order_by('margin_ratio')
    naver = get_naver(request)

    for item in item_list:
        naver_info = naver.get_item_info(item.naver_id)
        if naver_info:
            item.update_with_naver_info(naver_info)
            item.save()          
    return redirect(reverse('store:index'))

def print_from_dict(item_dict, key):
    if item_dict[key]:
        print(item_dict['scout_category'])
    else:
        print(str(key)+" 아이템이 없어서 출력할 수 없음")

def check_tag(request):
    item_list = ItemData.objects.filter(user=request.user, category_score__gt=0).order_by('-category_score', 'modify_date')
    #item_list = [item_list[0]]
    check_category_item_list(request, item_list, depth=1)
    return redirect(reverse('store:index'))

def depth_print(input_str="", depth=0):
    indent = ""
    for i in range(depth):
        indent += "  "
    print(indent + "[View] " + input_str)

def check_category_item(request, item, depth=0, scout=None, naver=None):
    item_dict = None

    is_delete = False
    while ((not item_dict) or (not 'naver_category' in item_dict) or (item_dict['naver_category'] is None)):
        item_dict = vars(item)
        (naver_result, item_dict) = naver.get_category(item_dict, depth=depth+1, with_save=False)
        if naver_result == True and not item_dict:
            depth_print("네이버에서 삭제된 아이템 삭제", depth=depth+1)
            if item.pk:
                item.delete()
            naver.cancel_item_page(depth=depth+1)
            is_delete = True
            return (False, item_dict)

    (scout_result, item_dict) = scout.get_category(item_dict, depth=depth+1)

    #print_from_dict(item_dict, 'naver_category')
    #print_from_dict(item_dict, 'scout_category')
    
    min_category_info=[99999,'']
    category_index = 1
    category_string_list = []
    for category in item_dict['scout_category']:
        weight = 1000
        score = 0

        # 카테고리 별 점수 책정
        for index in range(min(len(category), len(item_dict['naver_category']))):
            if category[index] != item_dict['naver_category'][index]:
                score = score + weight * category_index
            weight = weight / 10

        # 최적 카테고리 선택 루틴
        if min_category_info[0] > score:
            min_category_info[0] = score
            min_category_info[1] = ">".join(category)
            depth_print("카테고리 분석 최저점 달성 "+str(min_category_info), depth=depth+1)
        else:
            depth_print("최저점 달성 실패 점수: "+str(score)+" 카테고리 스트링: "+(">".join(category)), depth=depth+1)
        category_string_list.append(">".join(category))

    # 대분류 비수정으로 선택가능한 카테고리가 없는 경우
    item_dict['category_current'] = item_dict['naver_category']
    item_dict['category_list'] = category_string_list
    if min_category_info[0] < 9999:
        item_dict['category_score'] = min_category_info[0]
        item_dict['category_recommand'] = min_category_info[1]
    else: # 대분류 비수정으로 선택가능한 카테고리가 있을 경우
        item_dict['category_score'] = 99999
        if len(item_dict['category_list']) > 0:
            item_dict['category_recommand'] = item_dict['category_list'][0]
        else:
            item_dict['category_recommand'] = ""

    if min_category_info[0] > 0:
        if min_category_info[0] < 1000:
            depth_print("소분류 변경 필요", depth=depth+1)
            naver.set_recommand_category(item_dict, depth=depth+1)
            item.set_item_info(item_dict)
        elif min_category_info[0] < 9999:
            depth_print("대분류 변경 필요", depth=depth+1)
            naver.save_item_page(depth=depth+1)
            (result, new_item_dict) = naver.set_main_category(item_dict, depth=depth+1)
            if result == 1:
                new_item_dict['category_score'] = 0
                item.set_item_info(new_item_dict)
            elif result == -1:
                print("권한 제한 아이템 삭제")
                naver.delete_item_with_domeme_id(item_dict, depth=depth+1)
                item.delete()
        else:
            depth_print("카테고리를 획득하지 못한 경우 유저가 검색어를 조정해주어야 함", depth=depth+1)
            naver.save_item_page(depth=depth+1)
    else:
        # 카테고리 변경이 필요없을 때는 naver 페이지를 none으로 만들어두어야 다음 검색에 문제가 안생김
        naver.save_item_page(depth=depth+1)
    
    item.set_item_info(item_dict)

def check_category_item_list(request, item_list, depth=0):
    depth_print("check_category_item_list 콜", depth=depth+1)
    scout = Scout()
    naver = Naver()

    count = 0
    for item in item_list:
        process_print(count, len(item_list))
        (result, item_dict) = check_category_item(request, item, scout=scout, naver=naver, depth=depth+1)
        if not result:
            continue
        print()
        count = count + 1
        
    return redirect(reverse('store:index'))
        
def refresh_oldest(request):
    item_list = ItemData.objects.filter(user=request.user).order_by('modify_date')
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_unset_naver_edit_id(request):
    item_list = ItemData.objects.filter(user=request.user, naver_edit_id=-1).order_by('modify_date')
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_uncorrect_margin(request):
    item_list = ItemData.objects.filter(user=request.user, margin_ratio__lt=10).order_by('margin_ratio')
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_uncorrect_upper_margin(request):
    item_list = ItemData.objects.filter(user=request.user, margin_ratio__gt=25).order_by('-margin_ratio')
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_unset_naver_sale_price(request):
    item_list = ItemData.objects.filter(user=request.user, naver_sale=0, domeme_row_price=-1).order_by('-create_date')
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_item_list(request, item_list, depth=0):
    naver = get_naver(request)
    domeme = get_domeme(request)
    index = 0
    for item in item_list:
        print(str(index+1)+"/"+str(len(item_list))+" "+format(((index+1)/len(item_list)*100), "0.2f")+"%")
        refresh_item(request, domeme, naver, item, depth=depth+1)
        index = index + 1

def refresh_minimum_count_list(request):
    item_list = ItemData.objects.filter(user=request.user, minimum_count__gt=1)
    refresh_item_list(request, item_list)
    return redirect(reverse('store:index'))

def refresh_item(request, domeme, naver, item, depth=0, scout=None):
    domeme_info = domeme.get_item_info(item.domeme_id)
    if not domeme_info:
        print("[Domeme] "+str(item.domeme_id)+" 도매매에서 삭제된 페이지 제거")
        item.delete()
        return (False, None)
    
    naver_info = naver.get_item_info(vars(item), depth=depth+1)
    if not naver_info:
        print("[Naver] "+str(item.naver_id)+" 네이버에서 제거된 아이템 제거")
        item.delete()
        return (False, None)

    if item.naver_edit_id == -1 and naver_info['naver_edit_id'] != -1:
        (result, edit_dict) = naver.get_edit_id({'naver_id':item.naver_id})
        if 'naver_edit_id' in edit_dict and edit_dict['naver_edit_id'] != -1:
            item.naver_edit_id = edit_dict['naver_edit_id']
        print("네이버 에딧 아이디 업데이트: "+str(item.naver_id)+" => "+str(item.naver_edit_id))

    item.update_naver_price_from_info(naver_info)
    item.set_domeme_price(float(domeme_info['domeme_price']), float(domeme_info['domeme_row_price']))
    item.title = title_replace(request.user, item.title)

    item_dict = vars(item)
    (naver_price, naver_sale) = naver.set_price(item_dict, goto_page=False, depth=depth+1)
    if naver_price and naver_sale:
        print("변경된 네이버 가격: "+str(naver_price)+" - "+str(naver_sale))
        item.update_naver_price(naver_price, naver_sale)
    else:
        print("네이버에서 제거됨으로 인한 "+str(item.domeme_id)+" 물건 제거")
        item.delete()

    check_category_item(request, item, depth=depth+1, naver=naver, scout=scout)

def refresh_item_view(request, pk):
    item = ItemData.objects.get(user=request.user, pk=pk)

    domeme = get_domeme(request)
    naver = get_naver(request)

    refresh_item(request, domeme, naver, item)

    return redirect(reverse('store:index'))

def title_replace(user, title):
    title_replace_rules = TitleReplace.objects.filter(user=user).order_by('priority')

    temp_title = title
    for rule in title_replace_rules:
        before = rule.before.replace('\s',' ')
        after = rule.after.replace('\s', ' ')
        temp_title = temp_title.replace(before, after)    
    temp_title = temp_title.strip()

    return temp_title

def title_replace_with_search(request):
    search_text = request.POST['search_text']
    print("검색어: "+search_text)

    if search_text:
        item_list = ItemData.objects.filter(user=request.user, title__icontains=search_text)
    else:
        item_list = ItemData.objects.filter(user=request.user)

    if len(item_list) > 0:
        title_replace_with_list(request, item_list)
    return redirect(reverse('store:index'))    

def title_replace_view(request):
    item_list = ItemData.objects.filter(user=request.user)
    title_replace_with_list(request, item_list)
    return redirect(reverse('store:index'))

def process_print(count, list_length):
    print(str(timezone.now())+" 진행도 "+str(count+1)+"/"+str(list_length)+" "+format(((count+1)/list_length*100), ".2f")+"%")

def title_replace_with_list(request, item_list):
    title_replace_view_rules = TitleReplace.objects.filter(user=request.user).order_by('priority')
    naver = get_naver(request)

    count = 0
    for item in item_list:
        process_print(count, len(item_list))
        temp_title = item.title
        for rule in title_replace_view_rules:
            before = rule.before.replace('\s',' ')
            after = rule.after.replace('\s', ' ')
            temp_title = temp_title.replace(before, after)    
        temp_title = temp_title.strip()
        if not item.title == temp_title:
            print("상품명 치환 '"+item.title+"'->'"+temp_title+"'")
            item.title = temp_title
            (result, item_info) = naver.set_new_title(vars(item), depth=1)
            item.set_item_info(item_info)
        count = count + 1

def delete_duplicate_item(request):
    item_list = ItemData.objects.filter(user=request.user)

    domeme_list = []
    naver_list = []
    count = 0
    for item in item_list:
        process_print(count, len(item_list))
        if item.domeme_id in domeme_list or item.naver_id in naver_list:
            item.delete()
            count = count + 1
        else:
            domeme_list.append(item.domeme_id)
            naver_list.append(item.naver_id)
    return redirect(reverse('store:index'))