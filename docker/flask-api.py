import subprocess,json,sys,logging,os,shutil
from flask import Flask,request,jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/api/image-updates',methods=['POST'])
def handle_gh_image_webhook():
    data = request.get_json()
    head_commit_message = data["head_commit"]["message"]
    logger.info(f"New commit received:'{head_commit_message}'")
    if 'fluxcdbot@users.noreply.github.com' in str(data):
        commit_prefix = os.environ.get('COMMIT_PREFIX')
        logger.info(f"commit_prefix='{commit_prefix}'")
        if commit_prefix is not None and head_commit_message is not None and commit_prefix in head_commit_message:
            logger.info('This commit is about a fluxcd image update. Time to check that image has been correctly deployed in a new K8S Pod and running fine.')
            cwd = os.getcwd()
            print("Current working directory: {0}".format(cwd))
            src_file = '/gitops_storage/check-image-updates.sh'
            dest_dir = './'
            filename = os.path.basename(src_file)
            dest_file = os.path.join(dest_dir, filename)
            if not os.path.exists(dest_file):
                shutil.copy(src_file, dest_dir)
                os.chmod(dest_file, 0o755)
                print(f'{filename} copied and made executable')
            else:
                print(f'{filename} already exists in destination directory')
            subprocess.Popen(["./check-image-updates.sh", head_commit_message])
    return 'OK', 200

@app.route('/api/healthchecksio',methods=['POST'])
def forward_healthchecksio_notif():
    content = request.data.decode('utf-8')
    # Check if content contains "Healthchecks.io" and execute the script if it does
    if content and "Healthchecks.io" in content:
        cwd = os.getcwd()
        print("Current working directory: {0}".format(cwd))
        src_file = '/gitops_storage/healthchecks-forward-notif.sh'
        dest_dir = './'
        filename = os.path.basename(src_file)
        dest_file = os.path.join(dest_dir, filename)
        if not os.path.exists(dest_file):
            shutil.copy(src_file, dest_dir)
            os.chmod(dest_file, 0o755)
            print(f'{filename} copied and made executable')
        else:
            print(f'{filename} already exists in destination directory')
        subprocess.Popen(["./healthchecks-forward-notif.sh", content])
    return 'OK', 200

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=5001,debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)
