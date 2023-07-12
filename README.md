# Wallcome Home

***깃허브 Fianl 저장소의 main.py를 실행해 주세요.***

[trailer] https://youtu.be/VVgFnd9Zyew
[VMP_final.pdf](https://github.com/princesskim/Final/files/12022504/VMP_final.pdf)


<img width="1440" alt="1" src="https://github.com/princesskim/Final/assets/102868454/b0d0d842-747a-4f75-8d45-9429b045a565">
강아지의 울음소리인 '왈'과 'wellcome'을 합쳐 바깥 세상을 구경하러 나간 강아지들을 잡아오는 힐링게임의 제목 [Wallcome Home]을 지었다.
 
<img width="1440" alt="2" src="https://github.com/princesskim/Final/assets/102868454/6cfe799b-1120-4dd9-b3e5-d55b8bac82d8">
클릭을 하면 화면이 전환되도록 메인 루프 안에서 각 스크린을 부르는 플래그 변수를 선언하였다. 시작 화면 이후에 나오는 것은 게임의 컨셉과 게임 방법을 알려주는 튜토리올이다. 게임 유저는 호기심 많은 강아지의 주인이 된다.
 
<img width="1440" alt="3" src="https://github.com/princesskim/Final/assets/102868454/8dc1291d-724e-4877-87dc-f002bfab089d">
강아지들은 귀를 펄럭이면 날 수 있음을 발견하고 집을 탈출한다. 스페이스 바를 누르면 강아지가 날아다니는 모습을 볼 수 있다. 체험형 튜토리올을 통해 유저가 게임에 몰입하도록 한다.
 
<img width="1440" alt="4" src="https://github.com/princesskim/Final/assets/102868454/ca0bf4e1-5f8e-419a-aaf3-795640fbbf0c">
 
<img width="1440" alt="5" src="https://github.com/princesskim/Final/assets/102868454/4bc3a3ed-7b71-41cc-9810-99131ee4fed1">
게임 실행 전에 버블 발사대 조작 방법을 익힐 수 있도록 화살표와 스페이스 키를 사용하여 버블을 쏘는 튜토리올을 추가했다.
 
<img width="1440" alt="6" src="https://github.com/princesskim/Final/assets/102868454/786aecf2-383a-456f-ba41-8721636b4276">
바닥에 내려온 갇힌 강아지와 버블은 클릭하여 없앤다. 코드 상에서 완전히 사라지는 것은 아니고 클래스 안에 active 인자를 추가하여 draw 함수에서 active == False인 강아지와 버블은 그리지 않는다.만약 클릭하지 않으면 버블은 사라지고 강아지는 다시 자유롭게 날아다닌다.
 
<img width="1440" alt="7" src="https://github.com/princesskim/Final/assets/102868454/934c4a9d-cccf-44b5-8ba1-7854fc60054e">
튜토리올이 끝나면 게임이 진행된다. 10마리의 날아다니는 강아지를 모두 버블에 가둬 집으로 돌려보내야 한다.
 
<img width="1440" alt="8" src="https://github.com/princesskim/Final/assets/102868454/63825760-2bc3-42e3-b0a0-8253dc96be30">
버블과 강아지가 최초로 충동하면 강아지의 귀가 쫑긋한 모양으로 바뀌고, 버블 속에 갇힌 채로 천천히 바닥으로 내려온다. 강아지 클래스 안에 충돌을 계산하기 위한 센터를 지정해주었다. 강아지의 센터와 버블의 센터 사이 거리를 토대로 충돌을 감지할 수 있다.
 
<img width="1440" alt="9" src="https://github.com/princesskim/Final/assets/102868454/85f6620e-09fd-4025-87d4-48392193a0ed">
강아지가 버블 가운데에 있는 것처럼 보이지만 코드만으로 해석하면 버블이 강아지의 센터를 카피해서 중심으로 삼는다. 바닥에 닿을 때도 강아지~바닥과의 거리를 계산하여 계속 강아지가 버블 정중앙에 있도록 업데이트해준다.
 
<img width="1440" alt="10" src="https://github.com/princesskim/Final/assets/102868454/58c7d694-5c3c-43f0-a471-c16872a2637c">
모든 강아지를 집으로 돌려보내면 성공화면이 뜬다. 그리고 미니게임에 대한 안내가 시작된다.
 
<img width="1440" alt="11" src="https://github.com/princesskim/Final/assets/102868454/0d1c1828-f051-4511-b970-8df92f9ff39f">
미니게임의 룰은 위와 같다. 모든 강아지를 안전하게 데려온 유저에게 막내 강아지의 얼굴을 만들 수 있게 해주며 컨셉을 지킨다.
 
<img width="1440" alt="12" src="https://github.com/princesskim/Final/assets/102868454/576d4a50-f96a-4dff-81fe-d64996030f6e">
미니게임의 실행화면은 다음과 같다. 눈과 코가 없는 여백의 얼굴에 귀만 달려있고, 눈과 코를 쏘아올릴 cannon도 있다.
 
<img width="1440" alt="13" src="https://github.com/princesskim/Final/assets/102868454/98890c14-1abb-42ed-a257-7580add4256a">
눈에 해당하는 콩알만큼 작은 검은 원이 나옴을 볼 수 있다.
 
<img width="1440" alt="14" src="https://github.com/princesskim/Final/assets/102868454/759632c1-4c83-4de9-802e-567fccc0824f">
코에 해당하는 검은 타원 또한 발사됨을 볼 수 있다.
 
<img width="1440" alt="15" src="https://github.com/princesskim/Final/assets/102868454/07296de9-79cc-4040-928b-0f662b087a11">
원히는 위치에 다다르면 그 위치에 눈과 코를 고정시키는 고정키를 눌러준다. 얼굴이 완성되면 미니게임도 끝이다.


