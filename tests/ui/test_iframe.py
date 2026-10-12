
from playwright.sync_api import Page, expect


def test_payment_iframe(page: Page):
    page.set_content(r"""
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Nested iframe Demo</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 15px;
      background: #f0f4f8;
    }
    iframe {
      width: 100%;
      height: 330px;
      border: 2px solid #64748b;
      border-radius: 8px;
      margin-top: 15px;
    }
    input { padding: 8px; }
    button {
      padding: 8px 12px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <h2>Main Page</h2>
  <input id="mainInput" placeholder="Main page input">
  <button onclick="updateMain()">Update Main</button>
  <p id="mainResult">Waiting...</p>

  <iframe id="frame1"></iframe>

  <script>
    function updateMain() {
      const value = document.getElementById("mainInput").value;
      document.getElementById("mainResult").textContent =
        "Main: " + value;
      document.body.style.backgroundColor = "#dcfce7";
    }

    const level2 = `
      <!DOCTYPE html>
      <html>
      <body style="font-family:Arial;padding:15px;background:#fef3c7">
        <h3>iframe Level 2</h3>
        <input id="input2" placeholder="Level 2 input">
        <button onclick="update2()">Update Level 2</button>
        <p id="result2">Waiting...</p>

        <script>
          function update2() {
            const value = document.getElementById('input2').value;
            document.getElementById('result2').textContent =
              'Level 2: ' + value;
            document.body.style.backgroundColor = '#fbcfe8';
          }
        <\/script>
      </body>
      </html>
    `;

    const level1 = `
      <!DOCTYPE html>
      <html>
      <body style="font-family:Arial;padding:15px;background:#dbeafe">
        <h3>iframe Level 1</h3>
        <input id="input1" placeholder="Level 1 input">
        <button onclick="update1()">Update Level 1</button>
        <p id="result1">Waiting...</p>

        <iframe id="frame2"
          style="width:95%;height:190px;border:2px solid blue">
        </iframe>

        <script>
          function update1() {
            const value = document.getElementById('input1').value;
            document.getElementById('result1').textContent =
              'Level 1: ' + value;
            document.body.style.backgroundColor = '#bfdbfe';
          }
        <\/script>
      </body>
      </html>
    `;

    const frame1 = document.getElementById("frame1");
    frame1.srcdoc = level1;

    frame1.addEventListener("load", () => {
      const frame2 = frame1.contentDocument
        .getElementById("frame2");
      frame2.srcdoc = level2;
    });
  </script>

</body>
</html>
    """)

    frame1 = page.frame_locator(
        'iframe[id="frame1"]'
    )

    frame1_input = frame1.get_by_placeholder("Level 1 input")
    frame1_button = frame1.get_by_role("button",name="Update Level 1")
    frame1_result1 = frame1.locator("#result1")

    frame1_input.fill("123456789")
    frame1_button.click()
    expect(frame1_result1).to_have_text("Level 1: 123456789")


    frame2 = frame1.frame_locator('iframe[id="frame2"]')

    frame2_input = frame2.get_by_placeholder("Level 2 input")
    frame2_button = frame2.get_by_role("button",name="Update Level 2")

    frame2_input.fill("222222")
    frame2_button.click()
    frame2_result2 = frame2.locator("#result2")
    expect(frame2_result2).to_have_text("Level 2: 222222")

    expect(frame1_input).to_have_value("123456789")
