from flask import Flask, render_template, request, send_file
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():

    before = request.files["before"]
    after = request.files["after"]

    before_path = os.path.join(UPLOAD_FOLDER, "before.mp4")
    after_path = os.path.join(UPLOAD_FOLDER, "after.mp4")

    before.save(before_path)
    after.save(after_path)

    output = os.path.join(UPLOAD_FOLDER, "result.mp4")

    cmd = f"""
    ffmpeg -y -i {before_path} -i {after_path} -filter_complex "
    [0:v]scale=960:1080[v0];
    [1:v]scale=960:1080[v1];
    [v0][v1]hstack=inputs=2
    " {output}
    """

    subprocess.call(cmd, shell=True)

    return send_file(output, as_attachment=True)

if __name__ == "__main__":
    app.run()
