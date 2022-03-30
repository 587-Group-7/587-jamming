NAVIGATION = """
<div class="nav-wrapper">
    <div class="nav">
        <div class="left">
            <div class="nav-item">
                <a href="/">Home</a>
            </div>
            <div class="nav-item">
                <a href="/view_robots">Control Robot</a>
            </div>
            <div class="nav-item">
                <a href="/map">View RSSI Map</a>
            </div>
        </div>
        <div class="right" id="nocred">
            <div class="nav-item">
                <a href="/account">Create Account</a>
            </div>
            <div class="nav-item">
                <a href="/login">Login</a>
            </div>
        </div>
        <div class="right" id="cred">
            <div class="nav-item" style="cursor: pointer">
                <a onclick="logout()">Log Out</a>
            </div>
        </div>
        <script>
            const getCookie = (name) => {
                var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
                if (match) {
                    return match[2];
                } else return null;
            }

            const refresh = async () => {
                const token = getCookie('token');
                if (token === null) {
                    document.getElementById("nocred").style.display = "flex";
                    return
                }
                const res = await fetch('/user/refresh', {
                    method: 'POST', // or 'PUT'
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                })
                if (res.status === 200) {
                    json = await res.json();
                    document.cookie = `token=${json.access_token}`;
                    document.getElementById("cred").style.display = "inline";
                } else {
                    document.getElementById("nocred").style.display = "flex";
                }
            };

            refresh();

            const logout = async () => {
                const date = new Date();
                date.setTime(-1);
                const expires = `; expires=${date.toGMTString()}`;
                document.cookie = `token=${json.access_token}${expires}`;
                window.location.replace("/");
            };
        </script>
        <style>
            #cred, #nocred {
                display: none;
            }
        </style>
    </div>
</div>
"""
