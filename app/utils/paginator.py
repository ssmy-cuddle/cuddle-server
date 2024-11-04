from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query

# 제네릭 타입 변수 정의
ModelT = TypeVar("ModelT")  # 모델 타입을 제네릭하게 정의하기 위한 타입 변수
FilterT = TypeVar("FilterT")  # 필터 타입을 제네릭하게 정의하기 위한 타입 변수

# 페이지네이션 결과를 담는 클래스 정의
class Page(BaseModel):
    model_name: str  # 모델의 이름을 저장하는 필드
    items: List[dict]  # 직렬화된 결과 아이템 리스트
    has_more: bool  # 다음 페이지 존재 여부
    next_cursor: Optional[str]  # 다음 페이지를 조회하기 위한 커서 값 (없으면 None)

# 페이지네이터 클래스 정의
class Paginator(Generic[ModelT, FilterT]):
    def __init__(self, model, query: Query):
        self.model = model  # 모델 클래스 설정
        self._query = query  # 주 쿼리 설정

    # 페이지네이션 결과를 가져오는 메서드 정의
    def get_paginated_result(
        self,
        *,
        cursor: Optional[str] = None,  # 커서 값, 기본값은 None
        filters: Optional[List[FilterT]] = None,  # 필터 리스트, 기본값은 None
        sorts: Optional[List[str]] = None,  # 정렬 조건 리스트, 기본값은 None
        limit: int = 10,  # 한 번에 가져올 데이터의 수 제한, 기본값은 10
        direction: str = "after"  # 페이지네이션 방향, 기본값은 "after"
    ) -> Page:
        
        primary_key_column = list(self.model.__mapper__.primary_key)[0]  # 첫 번째 기본 키 컬럼 가져오기
        
        # 정렬 조건이 있는 경우 쿼리에 정렬 적용
        if sorts:
            self._query = self.sort(sorts, self._query)

        # 커서가 있는 경우 이후 또는 이전 데이터를 가져오기 위한 쿼리 설정
        if cursor:
            if direction == "after":
                self._query = self._query.filter(self.model.primary_key_column > cursor)
            else:
                self._query = self._query.filter(self.model.primary_key_column < cursor)

        # 필터가 있는 경우 필터를 쿼리에 적용
        if filters:
            for filter_ in filters:
                self._query = self.skim_through(filter_=filter_)


        # limit + 1을 설정하여 다음 페이지의 존재 여부를 확인할 수 있게 함
        items = self._query.limit(limit + 1).all()
        has_more = len(items) > limit

        # 필요한 만큼의 데이터만 반환
        response_items = items[:limit]
        next_cursor = response_items[-1].id if has_more else None

        # 페이지 객체 생성하여 반환
        return Page(
            model_name=self.model.__name__,
            items=[item.__dict__ for item in response_items],  # 직렬화 가능한 데이터로 변환
            has_more=has_more,
            next_cursor=next_cursor,
        )

    # 필터를 쿼리에 적용하는 메서드
    def skim_through(self, filter_: FilterT, query: Optional[Query] = None) -> Query:
        query = query or self._query  # 쿼리가 주어지지 않은 경우 기본 쿼리를 사용
        return query.filter(filter_)

    # 정렬 조건을 쿼리에 적용하는 메서드
    def sort(self, sorts: List[str], query: Query) -> Query:
        for sort in sorts:
            if sort.startswith("-"):
                query = query.order_by(getattr(self.model, sort[1:]).desc())  # 내림차순 정렬 적용
            else:
                query = query.order_by(getattr(self.model, sort).asc())  # 오름차순 정렬 적용
        return query

# 사용 예시
# from models import YourModel
# from sqlalchemy.orm import session
# query = session.query(YourModel)
# paginator = Paginator(YourModel, query)
# paginated_result = paginator.get_paginated_result(cursor="some_cursor", filters=[YourModel.some_field == 'value'], sorts=["-created_at"])

# 새로운 페이지네이션 함수를 호출하는 라우트 예시
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from services.post_service import get_paginated_posts
# router = APIRouter()
# @router.get("/posts")
# def get_posts_endpoint(cursor: Optional[str] = None, limit: int = 10, db: Session = Depends(get_db)):
#     result = get_paginated_posts(db=db, cursor=cursor, limit=limit)
#     return {
#         "items": result["items"],
#         "has_more": result["has_more"],
#         "next_cursor": result["next_cursor"]
#     }
