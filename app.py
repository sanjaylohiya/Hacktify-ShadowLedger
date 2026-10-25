

from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "shadowledger-dev-session-key-change-before-release"

# ShadowLedger challenge state
deployment_reviews = {
    "DEP-209": {
        "status": "Pending Review",
        "reviewer": "operations",
        "approved": False
    }
}

backup_approvals = {
    "BK-204": {
        "deployment_id": "DEP-209",
        "approved": False
    }
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok", "application": "ShadowLedger"}, 200

@app.route("/assets")

def assets():

    return render_template("assets.html")



@app.route("/staff")
def staff():
    query = request.args.get("q", "").strip()

    employees = [
        {"id": "ST-104", "name": "Alex Morgan", "department": "Operations"},
        {"id": "ST-208", "name": "Jordan Lee", "department": "IT Support"},
    ]

    if query:
        employees = [
            employee for employee in employees
            if query.lower() in employee["id"].lower()
            or query.lower() in employee["name"].lower()
            or query.lower() in employee["department"].lower()
        ]

    return render_template(
        "staff.html",
        query=query,
        employees=employees
    )


@app.route("/deployments")
def deployments():
    return render_template("deployments.html")
@app.route("/deployments/<deployment_id>")
def deployment_details(deployment_id):
    deployments_data = {
        "DEP-104": {
            "service": "Asset API",
            "status": "Completed"
        },
        "DEP-209": {
            "service": "Ledger Sync",
            "status": "Pending Review"
        }
    }

    deployment = deployments_data.get(deployment_id)

    if deployment is None:
        return "Deployment not found", 404

    return render_template(
    "deployment_details.html",
    deployment_id=deployment_id,
    deployment=deployment,
    review=deployment_reviews.get(deployment_id)
)
       

@app.route("/deployments/<deployment_id>/review", methods=["POST"])
def review_deployment(deployment_id):
    if "username" not in session:
        return redirect("/login")

    review = deployment_reviews.get(deployment_id)

    if review is None:
        return "Deployment review not found", 404

    if review["approved"]:
        return "Deployment already approved", 409

    reviewer = request.form.get("reviewer", "").strip()

    if not reviewer:
        return "Reviewer is required", 400

    # Intentional lab weakness:
    # Reviewer identity is trusted from the submitted form.
    if reviewer != review["reviewer"]:
        return "Reviewer not authorized", 403

    review["approved"] = True
    review["status"] = "Approved"

    return redirect(f"/deployments/{deployment_id}")

@app.route("/backups")
def backups():
    return render_template("backups.html")

@app.route("/backups/<backup_id>")
def backup_details(backup_id):
    backups_data = {
        "BK-101": {
            "system": "Asset Database",
            "status": "Restricted",
            "deployment_id": None
        },
        "BK-204": {
            "system": "Ledger Archive",
            "status": "Pending Review",
            "deployment_id": "DEP-209"
        }
    }

    backup = backups_data.get(backup_id)

    if backup is None:
        return "Backup not found", 404

    return render_template(
        "backup_details.html",
        backup_id=backup_id,
        backup=backup
    )

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "analyst" and password == "ShadowLab-2026":
            session["username"] = username
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/backups/BK-204/approve", methods=["POST"])
def approve_backup():
    if "username" not in session:
        return redirect("/login")

    if not deployment_reviews["DEP-209"]["approved"]:
        return "Deployment approval required", 403

    if backup_approvals["BK-204"]["approved"]:
        return "Archive already approved", 409

    approver = request.form.get("approver", "").strip()

    if not approver:
        return "Archive approver is required", 400

    # Intentional vulnerability:
    # The application trusts the submitted approver name
    # instead of checking the authenticated user's role.
    if approver != "archive_manager":
        return "Archive approver not authorized", 403

    backup_approvals["BK-204"]["approved"] = True
    return redirect("/backups/BK-204")


@app.route("/backups/BK-204/archive")
def ledger_archive():
    if "username" not in session:
        return redirect("/login")

    if not deployment_reviews["DEP-209"]["approved"]:
        return "Deployment review required", 403

    if not backup_approvals["BK-204"]["approved"]:
        return "Backup approval required", 403

    return (
        "ShadowLedger — Ledger Archive Released\n"
        "FLAG{shadowledger_review_chain_complete}",
        200,
        {"Content-Type": "text/plain; charset=utf-8"}
    )

@app.route("/admin/reset-lab", methods=["POST"])
def reset_lab():
    # Only allow reset requests from the VM itself.
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return "Local reset only", 403

    deployment_reviews["DEP-209"]["approved"] = False
    deployment_reviews["DEP-209"]["status"] = "Pending Review"
    backup_approvals["BK-204"]["approved"] = False

    return "ShadowLedger lab reset successfully", 200    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
