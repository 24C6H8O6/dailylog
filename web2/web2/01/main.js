const toggleBtn = document.querySelector('.toggleBtn');
const menu = document.querySelector('.navbar_menu');
const login = document.querySelector('.navbar_login');


toggleBtn.addEventListener('click', ()=>{
    menu.classList.toggle('active');
    login.classList.toggle('active');
});

const slides = document.querySelector('.slides'); //전체 슬라이드 컨테이너
const slideImg = document.querySelectorAll('.slides li'); //모든 슬라이드들
let currentIdx = 0; //현재 슬라이드 index
const slideCount = slideImg.length; // 슬라이드 개수
const prev = document.querySelector('.prev'); //이전 버튼
const next = document.querySelector('.next'); //다음 버튼
const slideWidth = 1000; //한개의 슬라이드 넓이
const slideMargin = 0; //슬라이드간의 margin 값

//전체 슬라이드 컨테이너 넓이 설정
slides.style.width = slideWidth * slideCount + 'px';

function moveSlide(num) {
  slides.style.left = -num * 1000 + 'px';
  currentIdx = num;
}

prev.addEventListener('click', function () {
  /*첫 번째 슬라이드로 표시 됐을때는 
  이전 버튼 눌러도 아무런 반응 없게 하기 위해 
  currentIdx !==0일때만 moveSlide 함수 불러옴 */

  if (currentIdx !== 0) moveSlide(currentIdx - 1);
});

next.addEventListener('click', function () {
  /* 마지막 슬라이드로 표시 됐을때는 
  다음 버튼 눌러도 아무런 반응 없게 하기 위해
  currentIdx !==slideCount - 1 일때만 
  moveSlide 함수 불러옴 */
  if (currentIdx !== slideCount - 1) {
    moveSlide(currentIdx + 1);
  }
});



function moveSlide2(num) {
    slides.style.left = -num * 500 + 'px';
    currentIdx = num;
  }
  
  prev.addEventListener('click', function () {
    /*첫 번째 슬라이드로 표시 됐을때는 
    이전 버튼 눌러도 아무런 반응 없게 하기 위해 
    currentIdx !==0일때만 moveSlide 함수 불러옴 */
  
    if (currentIdx !== 0) moveSlid2(currentIdx - 1);
  });
  
  next.addEventListener('click', function () {
    /* 마지막 슬라이드로 표시 됐을때는 
    다음 버튼 눌러도 아무런 반응 없게 하기 위해
    currentIdx !==slideCount - 1 일때만 
    moveSlide 함수 불러옴 */
    if (currentIdx !== slideCount - 1) {
      moveSlide2(currentIdx + 1);
    }
  });


const form = document.querySelector('#form__wrap');
const checkAll = document.querySelector('.terms__check__all input');
const checkBoxes = document.querySelectorAll('.input__check input');
const submitButton = document.querySelector('button');

const agreements = {
  termsOfService: false,
  privacyPolicy: false,
  allowPromotions: false,
};

form.addEventListener('submit', (e) => e.preventDefault()); // 새로고침(submit) 되는 것 막음

checkBoxes.forEach((item) => item.addEventListener('input', toggleCheckbox));

function toggleCheckbox(e) {
  const { checked, id } = e.target;  
  agreements[id] = checked;
  this.parentNode.classList.toggle('active');
  checkAllStatus();
  toggleSubmitButton();
}

function checkAllStatus() {
  const { termsOfService, privacyPolicy, allowPromotions } = agreements;
  if (termsOfService && privacyPolicy && allowPromotions) {
    checkAll.checked = true;
  } else {
    checkAll.checked = false;
  }
}

function toggleSubmitButton() {
  const { termsOfService, privacyPolicy } = agreements;
  if (termsOfService && privacyPolicy) {
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
  }
}

checkAll.addEventListener('click', (e) => {
  const { checked } = e.target;
  if (checked) {
    checkBoxes.forEach((item) => {
      item.checked = true;
      agreements[item.id] = true;
      item.parentNode.classList.add('active');
    });
  } else {
    checkBoxes.forEach((item) => {
      item.checked = false;
      agreements[item.id] = false;
      item.parentNode.classList.remove('active');
    });
  }
  toggleSubmitButton();
});

