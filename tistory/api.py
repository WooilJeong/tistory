import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class Tistory:
    """
    티스토리 오픈 API 클래스
    """
    def __init__(self, blog_url, client_id, client_secret):
        """
        티스토리 API 설정
        blog_url: 블로그 URL
        client_id: 클라이언트 ID
        client_secret: 클라이언트 SECRET
        authentication_url: 인증 URL
        """
        self.blog_url = blog_url
        self.blog_name = blog_url.split("//")[1].split(".")[0]
        self.client_id = client_id
        self.client_secret = client_secret
        self.authentication_url = f"https://www.tistory.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.blog_url}&response_type=code"
        print(self.authentication_url)


    def init_access_token(self, authentication_code):
        """
        Access Token 초기화
        authentication_code: Auth 코드
        """
        self.authentication_code = authentication_code
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.blog_url,
            "code": self.authentication_code,
            "grant_type": "authorization_code",
        }

        res = requests.get("https://www.tistory.com/oauth/access_token", params=params)

        if res.status_code == 200:
            self.access_token = res.text.replace("access_token=","")
            print("액세스 토큰 초기화 완료")
        else:
            print(f"액세스 토큰 초기화 오류(CODE:{res.status_code})")
    

    def blog_info(self):
        """
        블로그 정보
        """
        url = f"https://www.tistory.com/apis/blog/info?access_token={self.access_token}&output=json"
        res = requests.get(url)
        return res.json()


    def list_post(self, page_number):
        """
        글 목록
        - page_number: 불러올 페이지 번호
        """
        url = f"https://www.tistory.com/apis/post/list?access_token={self.access_token}&blogName={self.blog_name}&page={page_number}&output=json"
        res = requests.get(url)
        return res.json()


    def read_post(self, post_id):
        """
        글 읽기
        - post_id: 글 ID
        """
        url = f"https://www.tistory.com/apis/post/read?access_token={self.access_token}&blogName={self.blog_name}&postId={post_id}&output=json"
        res = requests.get(url)
        return res.json()

    def write_post(self, **kwargs):
        """
        글 작성
        - title: 글 제목 (필수)
        - content: 글 내용
        - visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        - category: 카테고리 아이디 (기본값: 0)
        - acceptComment: 댓글 허용 (0, 1 - 기본값)
        - tag: 태그 (',' 로 구분)
        - password: 보호글 비밀번호
        - published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        """
        url = "https://www.tistory.com/apis/post/write?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        for k, v in kwargs.items():
            params[k] = v
        res = requests.post(url, data=params)
        return res.json()


    def modify_post(self, **kwargs):
        """
        글 수정
        - postId: 글 번호 (필수)
        - title: 글 제목 (필수)
        - content: 글 내용
        - visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        - category: 카테고리 아이디 (기본값: 0)
        - published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        - slogan: 문자 주소
        - tag: 태그 (',' 로 구분)
        - acceptComment: 댓글 허용 (0, 1 - 기본값)
        - password: 보호글 비밀번호
        """
        url = "https://www.tistory.com/apis/post/modify?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        for k, v in kwargs.items():
            params[k] = v
        res = requests.post(url, data=params)
        return res.json()


    def attach_post(self, uploadedfile):
        """
        파일 첨부
        - uploadedfile: 업로드할 파일 (multipart/form-data)
        """
        url = "https://www.tistory.com/apis/post/attach?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "uploadedfile": uploadedfile,
            "output": "json",
        }
        res = requests.post(url, data=params)
        return res.json()


    def list_category(self):
        """
        카테고리 목록
        """
        url = f"https://www.tistory.com/apis/category/list?access_token={self.access_token}&blogName={self.blog_name}&output=json"
        res = requests.get(url)
        return res.json()


    def newest_comment(self, page=1, count=10):
        """
        최근 댓글 목록
        - page: 가져올 페이지 (기본값: 1)
        - count: 페이지당 댓글 수 (기본값: 10, 최대값: 10)
        """
        url = f"https://www.tistory.com/apis/comment/newest?access_token={self.access_token}&blogName={self.blog_name}&page={page}&count={count}&output=json"
        res = requests.get(url)
        return res.json()


    def list_comment(self, post_id):
        """
        게시글 댓글 목록
        """
        url = f"https://www.tistory.com/apis/comment/list?access_token={self.access_token}&blogName={self.blog_name}&postId={post_id}&output=json"
        res = requests.get(url)
        return res.json()


    def write_comment(self, **kwargs):
        """
        댓글 작성
        - postId: 글 ID (필수)
        - parentId: 부모 댓글 ID (대댓글인 경우 사용)
        - content: 댓글 내용
        - secret: 비밀 댓글 여부 (1: 비밀댓글, 0: 공개댓글 - 기본 값)
        """
        url = "https://www.tistory.com/apis/comment/write?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        for k, v in kwargs.items():
            params[k] = v
        res = requests.post(url, data=params)
        return res.json()


    def modify_comment(self, **kwargs):
        """
        댓글 수정
        - postId: 글 ID (필수)
        - commentId: 댓글 ID (필수)
        - parentId: 부모 댓글 ID (대댓글인 경우 사용)
        - content: 댓글 내용
        - secret: 비밀 댓글 여부 (1: 비밀댓글, 0: 공개댓글 - 기본 값)
        """
        url = "https://www.tistory.com/apis/comment/modify?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        for k, v in kwargs.items():
            params[k] = v
        res = requests.post(url, data=params)
        return res.json()


    def delete_comment(self, **kwargs):
        """
        댓글 삭제
        - postId: 글 ID (필수)
        - commentId: 댓글 ID (필수)
        """
        url = "https://www.tistory.com/apis/comment/delete?"
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        for k, v in kwargs.items():
            params[k] = v
        res = requests.post(url, data=params)
        return res.json()


class Auto:
    """
    티스토리 자동화 클래스
    """
    def __init__(self, kakao_id, kakao_pw, driver_path=None):
        """
        설정
        - kakao_id: 카카오 이메일
        - kakao_pw: 카카오 비밀번호
        - driver_path: 크롬 드라이버 경로
        """
        self.kakao_id = kakao_id
        self.kakao_pw = kakao_pw
        self.driver_path = driver_path
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")

    def get_access_token(self, authentication_url):
        """
        Access Token 조회
        - authentication_url: 인증 URL
        """
        # 크롬 드라이버 정의
        if self.driver_path:
            print("드라이버 경로 지정")
            self.driver = webdriver.Chrome(self.driver_path, options=self.options)
        else:
            print("드라이버 경로 미지정")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # 티스토리 로그인 페이지 접속
        self.driver.get(authentication_url)
        self.driver.implicitly_wait(10)
        random.randrange(1,4)
        self.driver.find_element(By.XPATH, """//*[@id="cMain"]/div/div/div/a[1]""").send_keys(Keys.ENTER)
        time.sleep(random.randrange(1,4))
        self.driver.find_element(By.XPATH, """//*[@id="id_email_2"]""").send_keys(self.kakao_id)
        time.sleep(random.randrange(1,4))
        self.driver.find_element(By.XPATH, """//*[@id="id_password_3"]""").send_keys(self.kakao_pw)
        time.sleep(random.randrange(1,4))
        self.driver.find_element(By.XPATH, """//*[@id="login-form"]/fieldset/div[8]/button[1]""").send_keys(Keys.ENTER)
        time.sleep(random.randrange(1,4))
        self.driver.find_element(By.XPATH, """//*[@id="contents"]/div[4]/button[1]""").send_keys(Keys.ENTER)
        time.sleep(random.randrange(1,4))
        current_url = self.driver.current_url
        authentication_code = current_url.split("code=")[1].split("&state=")[0]
        # 크롬 드라이버 종료
        self.driver.quit()
        return authentication_code
        
