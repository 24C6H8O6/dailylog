// 초기 설정

const express = require("express");
const router = express.Router();
const mysql = require("mysql");
const morgan = require("morgan");
const app = express();
const router2 = require("./router2");
app.use(morgan("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const body_parser = require("body-parser");
app.use(body_parser.json());
app.use(body_parser.urlencoded({ extended: false }));

const { response } = require("express");
const path = require("path");
app.set("view engine", "ejs");
// 경로 설정
app.set("views", __dirname + "/views");

// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// mysql 주소

// AWS RDS mysql 주소
// const conn = mysql.createConnection({
//   host: "database-2.cto6iphlk0yd.ap-northeast-2.rds.amazonaws.com",
//   user: "admin2",
//   password: "121104115",
//   port: "3306",
//   database: "auto_farming",
// });

// 로컬주소 mysql
const conn = mysql.createConnection({
  host: "127.0.0.1",
  user: "test",
  password: "*swy7751",
  port: "3306",
  database: "auto_farming",
});

// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// 루트페이지로 접속 시
router.get("/", function (req, res) {
  res.redirect("http://127.0.0.1:5501/smhrd/express/public/main1.html");
});

// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// 1 페이지

// Join 회원가입 기능구현하기
router.post("/Join", function (request, response) {
  let id = request.body.id;
  let pw = request.body.pw;
  let nick = request.body.nick;

  let sql = "insert into member(id, pw, nick) values(?, ?, ?)";

  conn.query(sql, [id, pw, nick], function (err, rows) {
    if (!err) {
      console.log("입력성공");
      response.redirect(
        "http://127.0.0.1:5501/smhrd/express/public/main1.html"
      );
    } else {
      console.log("입력실패" + err);
    }
  });
});

// 검색기능구현하기(추후 삭제 예정)
router.get("/SelectAll", function (request, response) {
  conn.connect();

  let sql = "select * from user_table";
  conn.query(sql, function (err, rows) {
    if (!err) {
      //console.log(rows);

      // respnse이하는 html로 화면에 표시됨
      response.writeHead(200, { "Content-Type": "text/html;charset=utf-8" });
      response.write("<html>");
      response.write("<body>");

      // console.log(rows[1].id);
      for (let i = 0; i < rows.length; i++) {
        response.write("ID : " + rows[i].user_id);
        response.write("PW : " + rows[i].user_pw);
      }

      response.write("</body>");
      response.write("</html>");
      response.end();
    } else {
      console.log("검색실패 : " + err);
    }
  });
});

// Login기능구현하기
router.post("/Login", function (request, response) {
  let id = request.body.id;
  let pw = request.body.pw;
  let sql = "select * from user_table where user_id = ? and user_pw = ? ";
  conn.query(sql, [id, pw], function (err, rows) {
    if (rows.length > 0) {
      console.log("로그인 성공 : " + rows.length);
    } else {
      console.log("로그인 실패 : " + rows.length);
    }
  });
});

// 2페이지

// get방식 센서데이터(farm_id 수정 필요)
// esp32에서 get방식으로 "http://로컬주소:8080/insertSensor" 에
// 센서데이터(temp, humd, height, rbheight, co2) 보내면
// 컴퓨터 서버에서 값을 받아 req.query로 tempi, humdi, heighti, rbheighti, co2i로 데이터 저장 후
// sql에 값 저장
// (farm_id 수정 필요)
router.get("/insertSensor", function (req, res) {
  console.log("사용자가 보낸 값 : " + req.query.temp);
  console.log("사용자가 보낸 값 : " + req.query.humd);
  console.log("사용자가 보낸 값 : " + req.query.wtheight);
  console.log("사용자가 보낸 값 : " + req.query.rbheight);
  console.log("사용자가 보낸 값 : " + req.query.co2);
  let tempi = req.query.temp;
  let humdi = req.query.humd;
  let wtheighti = req.query.wtheight;
  let rbheighti = req.query.rbheight;
  let co2i = req.query.co2;

  let sql =
    "insert into sensor_table(sensor_time, farm_id, tem_sensor, hum_sensor, wtuw_sensor, rbuw_sensor, co2_sensor) values(now(),'123',?,?,?,?,?)";

  conn.query(
    sql,
    [tempi, humdi, wtheighti, rbheighti, co2i],
    function (err, rows) {
      if (!err) {
        console.log("입력성공");
      } else {
        console.log("입력실패" + err);
      }
    }
  );
});

// DB에서 가장 최신의 센서 데이터 가져오기(가져온 값들 밖으로 빼기)
router.get("/selectSensor", function (req, res) {
  // let sql = "select temp, humd, wtuw, rbuw, co2 from sensor_table";
  let sql =
    "select * from (select * from sensor_table)a order by sensor_time desc limit 1;";

  conn.query(sql, function (err, rows) {
    //console.log(rows);
    if (!err) {
      console.log("조회성공");
      console.log(rows[0].tem_sensor);
      let tems = rows[0].tem_sensor;
      let humds = rows[0].hum_sensor;
      let wtuws = rows[0].wtuw_sensor;
      let rbuws = rows[0].rbuw_sensor;
      let co2s = rows[0].co2_sensor;
      res.render("index.ejs", {
        tem: tems,
        humd: humds,
        wtuw: wtuws,
        rbuw: rbuws,
        co2: co2s,
      });
    } else {
      console.log("조회실패 : " + err);
    }
  });
});

// 액츄에이터 작동여부 수신 후 DB에 업데이트
router.post("/updateAct", function (req, res) {
  let wtvalve_act = req.body.wtvalve_act;
  let awvalve_act = req.body.awvalve_act;
  let ac_act = req.body.ac_act;
  let o2gen_act = req.body.o2gen_act;
  let vent_act = req.body.vent_act;
  let veyor_act = req.body.veyor_act;
  let led1_act = req.body.led1_act;
  let led2_act = req.body.led2_act;
  let robot_act = req.body.robot_act;

  let sql =
    "update actuator_table set act_time=now() wtvalve_act=? awvalve_act=? ac_act=? o2gen_act=? vent_act=? veyor_act=? led1_act=? led2_act=? robot_act=? where id = '123'";

  conn.query(
    sql,
    [
      wtvalve_act,
      awvalve_act,
      ac_act,
      o2gen_act,
      vent_act,
      veyor_act,
      led1_act,
      led2_act,
      robot_act,
    ],
    function (err, rows) {
      if (!err) {
        console.log("수정성공");
        res.redirct("http://127.0.0.1:5501/smhrd/express/public/main1.html");
      } else {
        console.log("수정실패" + err);
      }
    }
  );
});

// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// btn1~btn9 : 물통밸브, 급수밸브, 에어컨적외선, 산소수, 환기적외선, 컨베이어, LED1, LED2, 로봇

router.get("/test1", function (require, response) {
  // toggle();
  response.send(a1);
  console.log(a1);
});

router.get("/auto", function (req, res) {
  req.params(test2.a);
});

var a1 = 0;
router.get("/btn1", function (req, res) {
  function btn1() {
    if (a1 == 1) {
      a1 = 0;
    } else if (a1 == 0) {
      a1 = 1;
    }
    res.redirect(`http://127.0.0.1:8080/btn1?data=${a1}`);
  }
});

// ------------------------------------------------------
// ------------------------------------------------------
// icalendar

const ics = require("ics");
require("dotenv").config({ path: "nodemailer/.env" }); // nodemailer 폴더에 있는 .env 파일을 찾아서 환경변수를 설정
const nodemailer = require("./nodemailer"); // nodemailer 폴더의 index.js

const event = {
  start: [2021, 10, 30, 9, 30],
  duration: { hours: 1, minutes: 30 },
  title: "신제품 마케팅 회의",
  description: "신사업팀에서 개발한 신제품에 대한 해외 마케팅 회의",
  location: "더그레잇 3층",
  url: "http://thegreat.io",
  geo: { lat: 30.12, lon: 50.45 },
  organizer: { name: "Jeremy", email: "orgainizer@mail.com" },
  attendees: [
    {
      name: "참석자1",
      email: "addr1@mail.com",
      rsvp: true,
      role: "REQ-PARTICIPANT",
    },
    { name: "참석자2", email: "addr2@mail.com", role: "OPT-PARTICIPANT" },
  ],
};

const sendIcs = async () => {
  ics.createEvent(event, async (error, value) => {
    if (error) {
      console.log(error);
      return;
    }

    let message = {
      from: "seungwon.go@gmail.com", // 보내는 사람 주소
      to: "seungwon.go@returnvalues.com", // 받는 사람 주소
      subject: "신제품 마케팅 회의", // 이메일 제목
      text: "신사업팀에서 개발한 신제품에 대한 해외 마케팅 회의", // 이메일 내용
      icalEvent: {
        filename: "invitation.ics", // iCalendar 첨부 파일 명
        method: "REQTUEST", // REQUEST-요청, CACEL-취소
        content: value, // iCalendar 이벤트
      },
    };
    const r = await nodemailer.send(message); // 이메일 발송
  });
};

sendIcs();
module.exports = router;
// router에 대한 정보를 갖고있는 객체를 외부에서 사용할 수 있게 모듈화
