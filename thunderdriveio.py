import requests
import os


class ThunderClient(object):
    BASE_URL = "https://app.thunderdrive.io/secure/"

    def __init__(self, email, passwd):
        # First login
        self.session = requests.Session()
        self._login(email, passwd)
        self.user_id = self.get("drive/entries")["data"][0]["users"][0]["id"]  # ugly way to extract user id
        print(self.user_id)

    def _login(self, email, passwd):
        r = self.session.post(self.BASE_URL + "auth/login", data={"remember": False, "email": email, "password": passwd})
        r.raise_for_status()
        rdata = r.json()
        assert rdata['status'] == "success"

    def get(self, url, get_raw=False):
        r = self.session.get(self.BASE_URL + url)
        r.raise_for_status()
        if get_raw:
            return r
        return r.json()

    def post(self, url, **kwargs):
        r = self.session.post(self.BASE_URL + url, **kwargs)
        print(r.content, r.request.headers)
        r.raise_for_status()
        return r.json()

    def get_folders(self):
        return self.get("drive/users/{}/folders".format(self.user_id))["folders"]

    def get_space_usage(self):
        r = self.get("drive/user/space-usage".format(self.user_id))
        return r["used"], r["available"]

    def move_file(self):
        pass

    def create_folder(self, name, parent_id=None):
        pass

    def upload_file(self, fname, upload_name=None):
        if upload_name is None:
            upload_name = fname
        h = {'X-XSRF-TOKEN': self.get_xsrf() + "="}
        return self.post("uploads", headers=h, files={'file': (upload_name, open(fname, 'rb'))})

    def download_file(self, fname, outpath):
        if os.path.isdir(outpath):
            outpath = outpath + fname
        # TODO find hash from file_tree
        r = self.get("uploads/download?hashes={}".format("MTQ4OTY3MTB8cA"), get_raw=True)
        print(outpath)
        with open(outpath, "wb") as f:
            f.write(r.content)

    def get_xsrf(self):
        for cookie in self.session.cookies:
            if cookie.name == 'XSRF-TOKEN':
                return cookie.value
        raise Exception("Cookie not found.")

    def get_entities(self, add_params_from_url):
        pass

    def get_folder(self):
        pass

    def __getitem__(self, key):
        # return self.file_tree
        pass


if __name__ == "__main__":
    import secret
    cli = ThunderClient(secret.EMAIL, secret.PASS)
    print(cli.get_folders())
    print(cli.get_space_usage())
    # print(cli.upload_file("test.txt", upload_name="xyz232.txt"))
    cli.download_file("cebula.jpg", "./")
