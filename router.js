const express = require("express");
const router = express.Router();

var conn = mysql.createConnection({
  host: "database-2.czhwbelwlp5g.ap-northeast-2.rds.amazonaws.com",
  user: "admin",
  password: "121104115",
  port: "3306",
  database: "auto_farming",
});

// 루트페이지로 접속 시
router.get("/", function (req, res) {
  res.redirect("http://127.0.0.1:5501/smhrd/express/public/main1.html");
});

// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// let btn1 = 2;
// global.btn1 = btn1;

router.get("/response", function (request, response) {
  console.log("사용자가 보낸 값 : " + request.query.site);

  response.redirect("http://192.168.70.56:5501/smhrd/express/public/ex04.html");
  // 외부/내부 해당페이지로 이동

  // 네이버/구글/다음 사용자가 선택한 값으로 사이트를 이동시키시오.
});

// post방식
router.post("/post", function (request, response) {
  console.log("사용자가 보낸 값 : " + request.body.text);
});

var mysql = require("mysql"); // 설치한 mysql기능
const { response } = require("express");
// 사용자가 보낸 값이 post방식일 때 분석해주는 express기능

// Join 기능구현하기
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

// test 해봄
router.post("/test", function (request, response) {
  let id = request.body.id;
  console.log("yes");
});

// Delete 기능구현하기
router.post("/Delete", function (request, response) {
  let id = request.body.id;
  let pw = request.body.pw;
  let nick = request.body.nick;

  let sql = "delete from member where id =?";

  conn.query(sql, [id], function (err, rows) {
    if (!err) {
      console.log("삭제성공");
      response.redirct("http://127.0.0.1:5501/smhrd/express/public/main1.html");
    } else {
      console.log("삭제실패" + err);
    }
  });
});

// Update 기능구현하기
router.post("/Update", function (request, response) {
  let id = request.body.id;
  let update = request.body.update;
  let data = request.body.data;

  let sql = "";

  if (update == "pw") {
    sql = "update member set pw = ? where id = ?";
  } else if (update == "nick") {
    sql = "update member set nick = ? where id = ?";
  }

  conn.query(sql, [data, id], function (err, rows) {
    if (!err) {
      console.log("수정성공");
      response.redirct("http://127.0.0.1:5501/smhrd/express/public/main1.html");
    } else {
      console.log("수정실패" + err);
    }
  });
});

// 검색기능구현하기
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

router.post("/OneSelect", function (request, response) {
  let id = request.body.id;

  let sql = "select * from user_table where user_id = ?";
  conn.query(sql, [id], function (err, rows) {
    if (!err) {
      //console.log(rows);

      response.writeHead(200, { "Content-Type": "text/html;charset=utf-8" });
      response.write("<html>");
      response.write("<body>");

      for (let i = 0; i < rows.length; i++) {
        response.write("ID : " + rows[i].id);
        // response.write("PW : " + rows[i].pw);
        // response.write("NICK : " + rows[i].nick);
      }

      response.write("</body>");
      response.write("</html>");
      response.end();
    } else {
      console.log("검색실패 : " + err);
    }
  });
});
// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------

// ★★ 여기서부터 진짜 ★★

// 11월 9일 수요일
// 선물2 -> insert_db
// post방식으로 sensor값(온도,습도,수위초음파,로봇초음파,CO2)을 json 방식으로 받아왔을 때
// mysqlDB에 저장

// router.post("/insert_sensor", function (req, res) {
//   let param1 = req.body.sensor;
//   let temp = param1.tem_sensor;
//   let humd = param1.hum_sensor;
//   let wtuw = param1.wtuw_sensor;
//   let rbuw = param1.rbuw_sensor;
//   let co2 = param1.co2_sensor;
//   let sql =
//     "insert into sensor_table(temp, humd, wtuw, rbuw, co2) values(?, ?, ?, ?, ?)";

//   conn.query(sql, [temp, humd, wtuw, rbuw, co2], function (err, rows) {
//     if (!err) {
//       console.log("입력성공");
//     } else {
//       console.log("입력실패" + err);
//     }
//   });
// });

// Login기능구현하기
router.post("/Login", function (request, response) {
  let id = request.body.id;
  let pw = request.body.pw;
  let sql = "select * from user_table where user_id = ? and user_pw = ?";

  conn.query(sql, [id, pw], function (err, rows) {
    // rows.length
    if (rows.length > 0) {
      console.log("로그인 성공 : " + rows.length);
      response.redirect(
        "http://127.0.0.1:5501/smhrd/express/public/ex06S.html"
      );
    } else {
      console.log("로그인 실패 : " + rows.length);
      response.redirect(
        "http://127.0.0.1:5501/smhrd/express/public/ex06F.html"
      );
    }
  });
});

// get방식 센서데이터(farm_id 수정 필요)
router.get("/insertSensor", function (req, res) {
  console.log("사용자가 보낸 값 : " + req.query.temp);
  console.log("사용자가 보낸 값 : " + req.query.humd);
  console.log("사용자가 보낸 값 : " + req.query.height);
  console.log("사용자가 보낸 값 : " + req.query.co2);
  let temp = req.query.temp;
  let humd = req.query.humd;
  let height = req.query.height;
  let co2 = req.query.co2;
  let sql =
    "insert into sensor_table(sensor_time, farm_id, tem_sensor, hum_sensor, wtuw_sensor, rbuw_sensor, co2_sensor) values(now(),'123',?,?,?,'1',?)";

  conn.query(sql, [temp, humd, height, co2], function (err, rows) {
    if (!err) {
      console.log("입력성공");
    } else {
      console.log("입력실패" + err);
    }
  });
});

// DB에서 가장 최신의 센서 데이터 가져오기(가져온 값들 밖으로 빼기)
router.get("/selectSensor", function (req, res) {
  // let sql = "select temp, humd, wtuw, rbuw, co2 from sensor_table";
  conn.connect();
  let sql =
    "select * from (select * from sensor_table)a order by sensor_time desc limit 1;";
  conn.query(sql, function (err, rows) {
    if (!err) {
      console.log("조회성공");
      console.log(rows[0].wtuw_sensor);
      tem = rows[0].tem_sensor;
      var humd = rows[0].humd_sensor;
      var wtuw = rows[0].wtuw_sensor;
      var rbuw = rows[0].rbuw_sensor;
      var co2 = rows[0].co2_sensor;
      document.getElementById("data").innerHTML = tem;
      return tem, humd, wtuw, rbuw, co2;
    } else {
      console.log("조회실패 : " + err);
    }
  });
});
var tem = tem;

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
var a1;

function btn1(a) {
  a1 = string(a.checked);
  if (a.checked == true) {
    console.log(a.checked);
  } else {
    console.log(a.checked);
  }
}

router.get("/test1", function (require, response) {
  // toggle();
  response.send(a1);
  console.log(a1);
});

function btn2(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn3(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn4(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn5(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn6(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn7(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn8(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

function btn9(a) {
  this.a = a;
  if (a.checked == true) {
    console.log(a.checked);
    // let gg = "true";
  } else {
    console.log(a.checked);
    // let gg = "false";
  }
}

module.exports = router;
// router에 대한 정보를 갖고있는 객체를 외부에서 사용할 수 있게 모듈화
