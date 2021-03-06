# modelgirls

> VITON-HD를 이용한 무신사 제품 가상 피팅 서비스 (2021학년도 2학기 기계학습 팀 프로젝트)

아래 사진 클릭 시 서비스 발표 영상으로 이동합니다😉

[![발표영상](https://img.youtube.com/vi/l_vVrk0tgFQ/hqdefault.jpg)]( https://youtu.be/l_vVrk0tgFQ)



-----



## 개발 필요성

코로나 시대가 도래하며 사회는 비대면 활동을 권장하게 되었고, 이러한 상황에서 현대 사회의 온라인 쇼핑몰의 선호도 및 사용률은 빠르게 상승하고 있다. 2017년 온라인 쇼핑 시장 성장 전망은 78조 2000억이었으나, 2021년 온라인 쇼핑 시장 성장 전망은 199조이며 2022년에는 199조 8000억까지 기대되는 상황이다.(‘패션업계의 최신 트렌드는 ‘온라인’에서 답 찾기, 차완용, 매거진 한경, 2020.01.21)

하지만 온라인 쇼핑몰의 사용률이 증가함과 동시에 온라인 쇼핑몰의 치명적인 단점이 대두되고 있다. 오프라인 쇼핑이 아니니만큼 직접 제품을 살펴보거나 피팅해볼 수 없다는 점, 그리고 이로 인한 반품률 및 환불율이 높다는 점이다. 사업자 입장에서는 반품 및 교환을 진행한 제품을 정가로 재판매하기 어려우니, 반품된 제품은 그대로 폐기 처리를 하거나 헐값에 판매를 하며 손실을 본다. 반품 과정에서 소모되는 배송비는 연간 3000억으로, 사업자 입장에서는 절대 무시할 수 없는 손실이 발생하는 것이다. 소비자 또한 번거로운 반품 및 환불 과정이 즐겁지는 않다. 심지어 일부 온라인 업체에서는 소비자가에 반품 예상 손실분을 계산에 넣어 판매하는 경우도 있으니, 소비자는 가격적인 측면에서도 피해를 보고 있을 수 있는 것이다. ([김주식 전문기자의 유통 24時] 국내 반품규모 2조원대 넘어, 김주식, 파이낸셜 뉴스, 2007.08.20)

이러한 단점은 특히 의류 쇼핑몰에서 더욱 두드러진다. 직접 제품을 입어볼 수 없다는 단점이 크게 작용하는 탓이다. 실제로 의류 온라인 쇼핑몰의 반품률은 아주 높은 편이고, 반품의 이유로는 주로 생각했던 핏, 색감, 사이즈가 아닌 것 등이 있다. 그리고 우리의 가상 피팅 서비스는 이러한 문제를 해소할 수 있을 것으로 예측된다.



-----



## 개발 목표

대한민국 대표 온라인 패션커머스 기업인 **무신사스토어** 에 사용자의 사진과 의류 사진을 합성하는 가상 피팅 서비스를 제공한다. (사진 출처 : https://store.musinsa.com/app/goods/903340)

![image](https://user-images.githubusercontent.com/60170358/141873964-074b6ea2-a2a6-4c67-9a4f-14ee24a52df6.png)



------



## 구현 기술

### VITON-HD

**VITON-HD 공식 github:** https://github.com/shadow2496/VITON-HD

![image](https://user-images.githubusercontent.com/60170358/141874516-da72366b-e474-43e7-bdd9-edff84859b07.png)

**Dataset**

이미지 기반 virtual try-on 모델으로, 원하는 옷 이미지로 사용자의 상의를 가상피팅한다. dataset은 온라인 쇼핑몰 웹사이트에서 13,679의 여성 정면과 상의 이미지를 크롤링 하였다.  고해상도 구현을 위해 1024x768 해상도의 이미지를 수집하였고, Train dataset 11,647개와 Test dataset 2,032개로 나누었다. 

![image](https://user-images.githubusercontent.com/60170358/141874312-be04ce8e-bd09-45c6-acf7-cb73c0e3abca.png)



크게 4개의 과정으로 구성되어 있다. 

(a) Pre-processing은 사람의 이미지가 주어지면 상의, 하의, 얼굴 등을 segmentation 한 이미지와 pose를 추출한 이미지를 생성하고 그 2개의 이미지로 상의를 없앤 이미지와 상의를 없앤 segmentation 이미지를 생성한다. 이때 U-net 기반의 모델을 사용하였다.

(b) Segmentation Generation는 (a)에서 만든 상의 없앤 이미지를 바탕으로 segmentation generator을 통해 target 옷의 이미지에 맞는 사람의 segmentation 이미지를 생성한다.

(c) Clothes Deformation는 target 옷 이미지를 사람의 pose에 맞게 자연스럽게 입히기 위해 warping 하여 사람 pose에 최대한 맞는 변형된 옷 이미지를 생성한다.

(d) Try-On Synthesis는 (a)+(b)+(c) 에서 생성된 이미지들을 바탕으로 ALIAS Generator 을 통해 사람의 이미지에 target 옷 이미지가 입혀진 최종 이미지를 생성한다.





![image](https://user-images.githubusercontent.com/60170358/141874088-4839dc63-4d7a-4d30-8a03-2712990f1782.png)



**ALIAS Generator**

기존 VITON과 구별되는 점은 마지막 (d) 부분인 Try-On Synthesis 부분에서 ALIAS Generator을 사용하였다. ALIAS Generator는 아래 사진과 같이 사람의 체형에 따른 이미지와 옷의 이미지가 matching 이 잘 일어나지 않는 부분(mismatching)도 잘 match 시켜주게 하는 생성 모델이다.



![image](https://user-images.githubusercontent.com/60170358/141748009-4df6d744-6cd3-44bc-b512-a107ec4cef12.png)



참고 문헌 : Choi, S., Park, S., Lee, M., & Choo, J. (2021). VITON-HD: High-Resolution Virtual Try-On via Misalignment-Aware Normalization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (pp. 14131-14140).



------



## 기대효과

**1.**  **기존 앱과의 차별성**

기존에 존재하는 유사한 서비스로는 의류 사이즈를 추천해주는 모바일 어플 ‘ZEYO’, 자신의 신체 치수에 맞는 아바타를 생성하여 맞춤형 가상 피팅 서비스를 제공하는 롯데홈쇼핑의 ‘유니사이즈 서비스’, LF몰의 ‘마이핏 서비스’ 등이 있다. 이러한 서비스는 사이즈를 결정하는 것에만 의미가 있을 뿐, 핏이나 분위기 등과 같은 세세하지만 중요한 요소들은 확인할 수 없다. 하지만 우리의 서비스는 실제 사용자의 사진에 가상 피팅을 하는 방식을 이용하기 때문에 기존의 서비스보다 더욱더 사용자 맞춤형인 서비스를 제공할 수 있다.



**2.**  **온라인 쇼핑 시장에서의 긍정적 영향**

우리는 가상 피팅 서비스를 통해 직접 제품을 피팅해볼 수 없다는 온라인 쇼핑몰의 단점을 보완할 수 있을 것이라고 생각한다. 이러한 단점이 보완된다면 반품률이 감소할 것이며, 반품 및 교환에 소모되는 비용이 절감될 것이다. 또한 기존에 직접 제품을 피팅해보지 못해 온라인 구매를 꺼렸던 소비자들의 온라인 소비를 활성화하는 데에도 도움이 될 것이다. 이는 사업자와 소비자 모두에게 긍정적인 영향을 줄 것이며, 온라인 쇼핑몰 시장이 발전하는 데에 큰 도움이 될 것이다.

 

**3.**  **사업화 모델**

첫 번째로 온라인 쇼핑몰 어플 및 사이트에 본 기술을 탑재하여 월 또는 연 단위로 이용료를 받는 방식이 있다. 이는 기존 온라인 쇼핑몰에 기술만을 제공하는 방식으로, 조금 더 편리하고 보편적으로 소비자에게 접근할 수 있을 것이라고 생각된다.

두 번째는 자체 어플을 제작한 뒤 쇼핑몰과 연결하여 서비스를 이용할 수 있도록 하는 방식이다. 해당 모델에서는 어플에 광고를 붙이는 방식으로 수익을 창출할 예정이다. 하지만 해당 방식은 아직 어떻게 쇼핑몰과 연결할지, 연결된 쇼핑몰의 제품에 어떻게 가상 피팅 서비스를 적용할지 등의 방안이 구체화되지 않은 상태이므로 조금 더 논의가 필요할 것으로 예상된다.

 

**4.**  **기술 보완점**

Failure cases를 통해 제품 위에 글씨가 있거나 복잡한 패턴이 있는 경우, 인물의 이미지와 타겟 의류의 이미지가 완벽하게는 매칭되지 않는 문제가 발생하는 것을 확인할 수 있었다. 이를 해결하기 위해 하이퍼 파라미터 조절 등이 필요할 것으로 판단된다. 

또한 Pose image 생성 부분이 기대만큼 원활하게 이루어지지 않아 VITON dataset에 있는 모델 이미지만 사용 가능하다는 한계가 있었다. 이는 더 많은 연구와 실험을 통해 해결해야할 것으로 판단된다.
