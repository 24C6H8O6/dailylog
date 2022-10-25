// express : nodejs를 이용해서 서버를 개발할 때 가장 많이 사용되는 프레임워크
// 폴더구성
// config : 프로젝트에 대한 모든 환경변수 정보 저장(ex. DB연결정보, 외부API Key값 등)
// public : 정적파일관리(HTML, CSS, JavaScript, Image 등)
// router : 서버경로설정
// views : 동적파일관리(ejs)
// app.js : 서버를 실행하기 위한 main파일

const express = require("express");  // express사용설정
const app = express();  // express 실행 후 app변수에 저장

const router = express.Router();  // router 기능사용설정
router.get("/test", function(request, response){
    console.log("/test 라우터실행")
});

router.get("/plus", function(request,response){
    console.log("/plus 라우터실행")
});

router.get("/cal", function(request,response){
    console.log("/cal 라우터실행")

    response.writeHead(200, {"Content-Type" : "text/html;charset=utf-8"});
    response.write("<html>");
    response.write("<body>");
    if(request.query.cal=="+"){
        response.write(request.query.num1 +"+"+request.query.num2 + "=" + (parseInt(request.query.num1)+parseInt(request.query.num2)))
    }else if(request.query.cal=="-"){
        response.write(request.query.num1 +"-"+request.query.num2 + "=" + (parseInt(request.query.num1)-parseInt(request.query.num2)))
    }
    response.write("</body>");
    response.write("</html>");
    response.end();
});

router.get("/Login", function(request, response){
    console.log("/Login 라우터호출")

    console.log("ID : " + request.query.id);
    console.log("PW : " + request.query.pw);
})

app.use(router);

app.listen(3001);