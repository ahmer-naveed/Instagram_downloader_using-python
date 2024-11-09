from flask import Flask, render_template, request, redirect, url_for, flash
import instaloader
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages
app.config["DOWNLOAD_FOLDER"] = "downloads"  # Folder to save videos

# Ensure the download folder exists
os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)

# Initialize Instaloader
loader = instaloader.Instaloader(dirname_pattern=app.config["DOWNLOAD_FOLDER"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_url = request.form["url"]

        if not post_url:
            flash("Please enter a valid Instagram URL", "error")
            return redirect(url_for("index"))

        try:
            # Extract the shortcode from the URL
            shortcode = post_url.split("/")[-2]

            # Fetch the post details using the shortcode
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            if post.is_video:
                # Download the video post
                loader.download_post(post, target=shortcode)
                flash("Video downloaded successfully!", "success")
            else:
                flash("This post does not contain a video.", "warning")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
