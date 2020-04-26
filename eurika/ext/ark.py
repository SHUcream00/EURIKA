'''
Scripts for Arknights
Author: SHUcream00 (https://github.com/SHUcream00)

'''
from itertools import chain, combinations


class aks():
    def __init__(self):
        self.elite = {'상급엘리트': {'시즈': 6, '샤이닝': 6, '나이팅게일': 6, '이프리트': 6, '엑시아': 6, '실버애쉬': 6,\
                '호시구마': 6, '사리아': 6}, '근거리':{'시즈': 6, '실버애쉬': 6, '호시구마': 6, '사리아': 6}, '원거리':\
                {'샤이닝': 6, '나이팅게일': 6, '이프리트': 6, '엑시아': 6}, '전위': {'실버애쉬': 6}, '의료': {'샤이닝': 6,\
                '나이팅게일': 6}, '선봉': {'시즈': 6}, '술사': {'이프리트': 6}, '저격': {'엑시아': 6}, '중장': {'호시구마': 6,\
                '사리아': 6}, '보조': {}, '특수': {}, '치유': {'샤이닝': 6, '나이팅게일': 6, '사리아': 6}, '지원': {'샤이닝': 6,\
                '나이팅게일': 6, '실버애쉬': 6, '사리아': 6}, '화력': {'시즈': 6, '엑시아': 6, '실버애쉬': 6, '호시구마': 6},\
                '범위공격': {'이프리트': 6}, '감속': {}, '생존': {}, '방어': {'호시구마': 6, '사리아': 6}, '약화': {'이프리트': 6},\
                '강제이동': {}, '통제': {}, '폭발력': {}, '소환': {}, '고속재배치': {}, '코스트회복': {'시즈': 6}, '로봇': {},\
                'agents': {'시즈': 6, '샤이닝': 6, '나이팅게일': 6, '이프리트': 6, '엑시아': 6, '실버애쉬': 6,\
                '호시구마': 6, '사리아': 6}}

        self.norm = {'초기': {'야토우': 2, '두린': 2, '12F': 2, '레인저': 2, '느와르혼': 2},\
                '엘리트': {'텍사스': 5, '지마': 5, '프틸롭시스': 5, '사일런스': 5, '와파린': 5,\
                '레드': 5, '만티코어': 5, '클리프하트': 5, '에프이터': 5, '프로방스': 5, '블루포이즌': 5,\
                '파이어워치': 5, '메테오리테': 5, '플라티나': 5, '프라마닉스': 5, '이스티나': 5, '메이어': 5,\
                '스펙터': 5, '인드라': 5, '니어': 5, '리스캄': 5, '벌칸': 5, '크로와상': 5},\
                '근거리': {'텍사스': 5, '지마': 5, '레드': 5, '만티코어': 5, '클리프하트': 5,\
                '에프이터': 5, '스펙터': 5, '인드라': 5, '니어': 5, '리스캄': 5, '벌칸': 5, '크로와상': 5, '스캐빈저': 4,\
                '비그나': 4, '그라벨': 4, '로프': 4, '쇼': 4, '도베르만': 4, '에스텔': 4, '무스': 4, '프로스트리프': 4,\
                '마토이마루': 4, '쿠오라': 4, '굼': 4, '매터호른': 4, '펭': 3, '바닐라': 3, '플룸': 3, '멜란사': 3, '비글': 3, '야토우': 2,\
                '느와르혼': 2, '캐슬-3': 1}, '원거리': {'프틸롭시스': 5, '사일런스': 5, '와파린': 5, '프로방스': 5, '블루포이즌': 5,\
                '파이어워치': 5, '메테오리테': 5, '플라티나': 5, '프라마닉스': 5, '이스티나': 5, '메이어': 5, '밀라': 4, '퍼퓨머': 4,\
                '헤이즈': 4, '기타노': 4, '시라유키': 4, '메테오': 4, '제시카': 4, '어스스피릿': 4, '하이비스커스': 3, '안셀': 3,\
                '라바': 3, '스튜어드': 3, '크루스': 3, '아드나키엘': 3, '오키드': 3, '두린': 2, '12F': 2, '레인저': 2, '랜싯-2': 1},\
                '전위': {'스펙터': 5, '인드라': 5, '도베르만': 4, '에스텔': 4, '무스': 4, '프로스트리프': 4, '마토이마루': 4, '멜란사': 3,\
                '캐슬-3': 1}, '의료': {'프틸롭시스': 5, '사일런스': 5, '와파린': 5, '밀라': 4, '퍼퓨머': 4, '하이비스커스': 3, '안셀': 3,\
                '랜싯-2': 1}, '선봉': {'텍사스': 5, '지마': 5, '스캐빈저': 4, '비그나': 4, '펭': 4, '바닐라': 4, '플룸': 3, '야토우': 2},\
                '술사': {'헤이즈': 4, '기타노': 4, '라바': 3, '스튜어드': 3, '두린': 2, '12F': 2}, '저격': {'프로방스': 5, '블루포이즌': 5,\
                '파이어워치': 5, '메테오리테': 5, '플라티나': 5, '시라유키': 4, '메테오': 4, '제시카': 4, '크루스': 3, '아드나키엘': 3,\
                '레인저': 2}, '중장': {'니어': 5, '리스캄': 5, '벌칸': 5, '크로와상': 5, '쿠오라': 4, '굼': 4, '매터호른': 4, '비글': 3,\
                '느와르혼': 2}, '보조': {'프라마닉스': 5, '이스티나': 5, '메이어': 5, '어스스피릿': 4, '오키드': 3}, '특수': {'레드': 5,\
                '만티코어': 5, '클리프하트': 5, '에프이터': 5, '그라벨': 4, '로프': 4, '쇼': 4}, '치유': {'프틸롭시스': 5, '사일런스': 5,\
                '와파린': 5, '니어': 5, '밀라': 4, '퍼퓨머': 4, '굼': 4, '하이비스커스': 3, '안셀': 3, '랜싯-2': 1}, '지원': {'지마': 5,\
                '프틸롭시스': 5, '와파린': 5, '도베르만': 4, '캐슬-3': 1}, '화력': {'만티코어': 5, '클리프하트': 5, '프로방스': 5,\
                '블루포이즌': 5, '파이어워치': 5, '플라티나': 5, '이스티나': 5, '인드라': 5, '리스캄': 5, '벌칸': 5, '스캐빈저': 4,\
                '비그나': 4, '헤이즈': 4, '메테오': 4, '제시카': 4, '도베르만': 4, '무스': 4, '프로스트리프': 4, '마토이마루': 4,\
                '플룸': 3, '스튜어드': 3, '크루스': 3, '아드나키엘': 3, '멜란사': 3}, '범위공격': {'메테오리테': 5, '스펙터': 5, '기타노': 4,\
                '시라유키': 4, '에스텔': 4, '라바': 3}, '감속': {'에프이터': 5, '이스티나': 5, '시라유키': 4, '어스스피릿': 4, '프로스트리프': 4,\
                '오키드': 3}, '생존': {'만티코어': 5, '스펙터': 5, '인드라': 5, '벌칸': 5, '제시카': 4, '에스텔': 4, '마토이마루': 4, '멜란사': 3},\
                '방어': {'니어': 5, '리스캄': 5, '벌칸': 5, '크로와상': 5, '그라벨': 4, '쿠오라': 4, '굼': 4, '매터호른': 4, '비글': 3},\
                '약화': {'메테오리테': 5, '프라마닉스': 5, '헤이즈': 4, '메테오':4}, '강제이동': {'클리프하트': 5, '에프이터': 5,\
                '크로와상': 5, '로프': 5, '쇼': 5}, '통제': {'텍사스': 5, '레드': 5, '메이어': 5}, '폭발력': {'파이어워치': 5},\
                '소환': {'메이어': 5}, '고속재배치': {'레드': 5, '그라벨': 4}, '코스트회복': {'텍사스': 5, '지마': 5, '스캐빈저': 4,\
                '비그나': 4, '펭': 3, '바닐라': 3, '플룸': 3}, '로봇': {'랜싯-2': 1, '캐슬-3': 1},\
                'agents': {'시즈': 6, '샤이닝': 6, '나이팅게일': 6, '이프리트': 6, '엑시아': 6, '실버애쉬': 6,\
                '호시구마': 6, '사리아': 6, '텍사스': 5, '지마': 5, '레드': 5, '만티코어': 5, '클리프하트': 5,\
                '에프이터': 5, '스펙터': 5, '인드라': 5, '니어': 5, '리스캄': 5, '벌칸': 5, '크로와상': 5, '스캐빈저': 4,\
                '비그나': 4, '그라벨': 4, '로프': 4, '쇼': 4, '도베르만': 4, '에스텔': 4, '무스': 4, '프로스트리프': 4,\
                '마토이마루': 4, '쿠오라': 4, '굼': 4, '매터호른': 4, '펭': 3, '바닐라': 3, '플룸': 3, '멜란사': 3, '비글': 3, '야토우': 2,\
                '느와르혼': 2, '캐슬-3': 1, '프틸롭시스': 5, '사일런스': 5, '와파린': 5, '프로방스': 5, '블루포이즌': 5,\
                '파이어워치': 5, '메테오리테': 5, '플라티나': 5, '프라마닉스': 5, '이스티나': 5, '메이어': 5, '밀라': 4, '퍼퓨머': 4,\
                '헤이즈': 4, '기타노': 4, '시라유키': 4, '메테오': 4, '제시카': 4, '어스스피릿': 4, '하이비스커스': 3, '안셀': 3,\
                '라바': 3, '스튜어드': 3, '크루스': 3, '아드나키엘': 3, '오키드': 3, '두린': 2, '12F': 2, '레인저': 2, '랜싯-2': 1}}

        self.krdict = {'고급특별채용': '상급엘리트', '특별채용': '엘리트', '신입': '초기', '디버프':'약화', '방어형': '방어', '누커': '폭발력',\
                        '생존형': '생존', '제어형': '제어', '코스트+': '코스트회복', '쾌속부활': '고속재배치', '힐링': '치유', '딜러': '화력',\
                        '가드': '전위', '뱅가드': '선봉', '디펜더': '중장', '서포터': '보조', '메딕': '의료', '스나이퍼': '저격', '스페셜리스트': '특수',\
                        '근거리': '근거리', '원거리': '원거리', '범위공격': '범위공격', '캐스터': '술사', '강제이동': '강제이동', '지원': '지원'}

        self.krname = {'메테오리테':'메테오라이트', '블루포이즌':'블루포이즌'}

    def recruit(self, slice, kr=False) -> dict:

        def powerset(iterable):
            '''powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)'''
            s = list(iterable)
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

        elite_token = '상급엘리트'

        if elite_token in slice: target_dict = self.elite
        else: target_dict = self.norm

        check = all(arg in target_dict for arg in slice)
        if not check or len(slice) > 5: return "FALSE"

        res, temp = {}, set()
        if len(slice) > 3: cands = list(combinations(slice,3))
        else: cands = list(combinations(slice, len(slice)))

        for i in cands:
            for j in powerset(i):
                if j and j not in res:
                    temp.add(j)

        for i in list(temp)[::-1]:
            intersect = set.intersection(*map(lambda x: set(target_dict[x]), i))
            if len(intersect) != 0:
                if elite_token in slice and elite_token not in i: continue
                elif kr == False: res['+'.join(i)] = ' '.join(sorted(list(intersect), key = lambda x: target_dict['agents'][x], reverse = True))
                else: res['+'.join(tuple(self.to_kor(i)))] = ' '.join(sorted(list(intersect), key = lambda x: target_dict['agents'][x], reverse = True))

        return res

    def list_possibles(self, chars) -> dict:
        check = all(arg in {**self.elite['agents'], **self.norm['agents']} for arg in chars)
        if not check: return "FALSE"

        res = {}
        for i in chars:
            if i in self.elite['agents']: target_dict = self.elite
            else: target_dict = self.norm
            res[i] = ' '.join({k for k, v in target_dict.items() if i in v and k != 'agents'})

        return res

    def prettify_res(self, *results) -> str:
        res = ''
        for i in results:
            text = ''
            for k, v in sorted(i.items(), key = lambda x: len(x[0]), reverse=True):
                text += '['+k+'] ' + v + '\n'
            res += text
        return res

    def to_jpn(self, tags) -> list:
        if not tags: return False
        return list(self.krdict.get(i,i) for i in tags)

    def to_kor(self, tags) -> list:
        if not tags: return False
        res = {k if v == i else '' for k,v in self.krdict.items() for i in tags}
        res.discard('')
        return list(res)

    def is_kor(self, tags)  -> bool:
        if not tags: return False
        print(list(x in self.krdict for x in tags))
        return True if all(x in self.krdict for x in tags) else False

#TEST DRIVER
if __name__ == "__main__":
    str = ['엘리트','약화','저격','근거리','범위공격']
    str_kor = ['고급특별채용','캐스터','뱅가드','누커','코스트+']
    str_elite = ['엑시아']
    str_norm = ['기타노']
    str2 = ['엑시아', '기타노', '사리아', '블루포이즌']
    str_kor = ['스페셜리스트', '강제이동']
    ark = aks()
    #print(a.recruit(str))
    #print(a.prettify_res(a.recruit(str)))
    target = str_kor
    check_language = ark.is_kor(target)
    clause1 = ark.recruit(ark.to_jpn(target), check_language)
    print(ark.to_jpn(target), ark.is_kor(target))
    print(clause1)
    if clause1 != "FALSE": print(ark.prettify_res(clause1))
    else:
        clause2 = ark.list_possibles(str2)
        if clause2 != "FALSE": print(ark.prettify_res(clause2))
        else: pass
