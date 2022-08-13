# tistory

[![PyPI Latest Release](https://img.shields.io/pypi/v/pykakao.svg)](https://pypi.org/project/pykakao/)
![](https://img.shields.io/badge/python-3.8-blue.svg)
![](https://img.shields.io/badge/requests-2.28.1-red.svg)
![](https://img.shields.io/badge/api-tistory-green.svg)


## 기여자

<div align="center">
    <table>
    <tr>
        <td align="center">
            <a href="https://github.com/wooiljeong">
            <img src="https://avatars.githubusercontent.com/u/38076110?v=4" width="100px;" alt=""/><br />
            <sub><b>정우일</b></sub></a><br />
        </td>
    </tr>
    </table>
</div>


## 소개

tistory는 티스토리 블로그 오픈 API를 파이썬으로 쉽게 이용할 수 있도록 돕는 오픈소스 라이브러리입니다. 


## 설치

```bash
pip install tistory
```

## 예시

```python
from tistory import Tistory
ts = Tistory(blog_url, client_id, client_secret)

authentication_code = ""
ts.init_access_token(authentication_code)

# 블로그 정보
ts.blog_info()

# 글
## 글 목록
page_number = 1
ts.list_post(page_number)

## 글 읽기
post_id = 10
ts.read_post(post_id)

## 글 작성
title = "제목"
content = "내용"
visibility = "3"
acceptComment = "1"
ts.write_post(title=title, 
              content=content, 
              visibility=visibility, 
              acceptComment=acceptComment)

## 글 수정
ts.modify_post(postId=11, title='수정', content='수정')

# 카테고리
ts.list_category()

# 댓글
## 최신 댓글 목록
ts.newest_comment()

## 댓글 목록
post_id=10
ts.list_comment(post_id)

## 댓글 작성
ts.write_comment(postId=10, content="댓글 내용")

## 댓글 수정
ts.modify_comment(postId=10, commentId=13172618, content="댓글 수정")

## 댓글 삭제
ts.delete_comment(postId=11, commentId=13172620)
```


## 참조

- [티스토리 오픈 API 신청](https://www.tistory.com/guide/api/manage/register)
- [티스토리 오픈 API 가이드](https://tistory.github.io/document-tistory-apis/)


<div align=center>

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fwooiljeong%2Ftistory&count_bg=%23FF6666&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>