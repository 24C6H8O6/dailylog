// express를 사용하기 위한 3가지 단계
// 1. 프로젝트의 정보가 기입되는 package.json파일생성
//  -> npm init
// 2. 프로젝트에 express 설치
//  -> npm install express --save
// 3. 폴더구성을 생성
//  -> config(환경설정), public(정적), router(경로), views(동적), app.js(메인)


const express = require("express");
const app = express();

const router = express.Router();
const body_parser = require("body-parser");
// 사용자가 보낸 값이 post방식일 때 분석해주는 express기능
app.use(body_parser.urlencoded({extended:false}))
// 서버에서 body-parser가능을 사용하겠다라고 선언

// get방식
router.get("/review", function(request, response){
    console.log("사용자가 보낸 값 : " + request.query.text);
})

// post방식
router.post("/post", function(request, response){
    console.log("사용자가 보낸 값 : " + request.body.text)
})

app.use(router);
app.listen(3001);