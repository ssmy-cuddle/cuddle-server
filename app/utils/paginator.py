from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query

# 제네릭 타입 변수 정의
ModelT = TypeVar("ModelT")  # 모델 타입을 제네릭하게 정의하기 위한 타입 변수
FilterT = TypeVar("FilterT")  # 필터 타입을 제네릭하게 정의하기 위한 타입 변수

# 페이지네이션 결과를 담는 클래스 정의
class Page(BaseModel):
    model_name: str  # 모델의 이름을 저장하는 필드
    main_query: Query  # 주 쿼리를 저장하는 필드
    object_count_query: Query  # 객체 수를 계산하는 쿼리를 저장하는 필드
    has_more_query_factory: callable  # 다음 페이지의 존재 여부를 확인하는 함수

# 페이지네이터 클래스 정의Paginator
class (Generic[ModelT, FilterT]):
    def __init__(self, model, query: Query):
        self.model = model  # 모델 클래스 설정
        self._query = query  # 주 쿼리 설정
        self._object_count_query = query  # 객체 수 쿼리도 초기에는 주 쿼리로 설정

    # 페이지네이션 결과를 가져오는 메서드 정의
    def get_paginated_result(
        self,
        *,
        cursor: Optional[str] = None,  # 커서 값, 기본값은 None
        filters: Optional[List[FilterT]] = None,  # 필터 리스트, 기본값은 None
        sorts: Optional[List[str]] = None,  # 정렬 조건 리스트, 기본값은 None
        limit: int = 10,  # 한 번에 가져올 데이터의 수 제한, 기본값은 10
        direction: str = "after"  # 페이지네이션 방향, 기본값은 "after"
    ):
        # 커서가 있는 경우 이후 또는 이전 데이터를 가져오기 위한 쿼리 설정
        if cursor:
            if direction == "after":
                edges_query = self.get_edges_after_query(cursor)  # 커서 이후의 데이터를 가져오는 쿼리
            else:
                edges_query = self.get_edges_before_query(cursor)  # 커서 이전의 데이터를 가져오는 쿼리
            self._query = self._query.filter(self.model.id.in_(edges_query))  # 쿼리에 커서 조건을 적용

        # 필터가 있는 경우 필터를 쿼리에 적용
        if filters:
            for filter_ in filters:
                self.skim_through(filter_=filter_)  # 주 쿼리에 필터 적용
                self._object_count_query = self.skim_through(
                    filter_=filter_, query=self._object_count_query  # 객체 수 쿼리에도 필터 적용
                )

        # 정렬 조건이 있는 경우 쿼리에 정렬 적용
        if sorts and len(sorts) > 0:
            self._query = self.sort(sorts, self._query)

        # limit + 1을 설정하여 다음 페이지의 존재 여부를 확인할 수 있게 함
        self._query = self._query.limit(limit + 1)

        # 페이지 객체 생성하여 반환
        return Page[ModelT](
            self.model.__name__,  # 모델 이름 설정
            main_query=self._query,  # 주 쿼리 설정
            object_count_query=self._object_count_query,  # 객체 수 쿼리 설정
            has_more_query_factory=lambda x, v: self.get_has_more_edges_query(
                top_cursor=x, bottom_cursor=v, filters=filters  # 다음 페이지 존재 여부 확인을 위한 쿼리 생성 함수
            ),
        )

    # 커서 이후의 데이터를 가져오는 쿼리 생성 메서드
    def get_edges_after_query(self, cursor: str):
        # 커서 이후의 데이터 ID를 가져오는 쿼리 구현
        # 예시로, id 기준으로 이후 데이터를 가져오는 쿼리를 작성합니다.
        return self._query.filter(self.model.id > cursor).subquery()

    # 커서 이전의 데이터를 가져오는 쿼리 생성 메서드
    def get_edges_before_query(self, cursor: str):
        # 커서 이전의 데이터 ID를 가져오는 쿼리 구현
        return self._query.filter(self.model.id < cursor).subquery()

    # 필터를 쿼리에 적용하는 메서드
    def skim_through(self, filter_: FilterT, query: Optional[Query] = None) -> Query:
        # 필터를 적용하는 로직을 구현합니다.
        query = query or self._query  # 쿼리가 주어지지 않은 경우 기본 쿼리를 사용
        return query.filter(filter_)  # 필터를 쿼리에 적용하여 반환

    # 정렬 조건을 쿼리에 적용하는 메서드
    def sort(self, sorts: List[str], query: Query) -> Query:
        # 정렬을 적용하는 로직을 구현합니다.
        # 예: sorts = ["created_at", "-name"] 이면 created_at 오름차순, name 내림차순 정렬
        for sort in sorts:
            if sort.startswith("-"):
                query = query.order_by(getattr(self.model, sort[1:]).desc())  # 내림차순 정렬 적용
            else:
                query = query.order_by(getattr(self.model, sort).asc())  # 오름차순 정렬 적용
        return query  # 정렬이 적용된 쿼리 반환

    # 다음 페이지 데이터가 있는지 확인하는 쿼리 생성 메서드
    def get_has_more_edges_query(self, top_cursor: str, bottom_cursor: str, filters: Optional[List[FilterT]] = None):
        # 다음 페이지 데이터가 있는지 확인하는 쿼리
        has_more_query = self._query.filter(self.model.id > bottom_cursor)  # 커서 이후의 데이터가 있는지 확인
        if filters:
            for filter_ in filters:
                has_more_query = self.skim_through(filter_, query=has_more_query)  # 필터를 적용하여 쿼리 생성
        return has_more_query  # 다음 페이지 확인 쿼리 반환

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
