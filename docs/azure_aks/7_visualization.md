# 7. visualization

## view camera heatmap

* check username of basic auth
```bash
mac:$ cat secrets/auth-tokens.json | jq '.basic_auths | map(select(.allowed_paths[] | contains ("/visualization/camera/heatmap"))) | .[0].username' -r
```

* check password of basic auth
```bash
mac:$ cat secrets/auth-tokens.json | jq '.basic_auths | map(select(.allowed_paths[] | contains ("/visualization/camera/heatmap"))) | .[0].password' -r
```

* open browser
```bash
mac:$ open https://api.tech-sketch.jp/visualization/camera/heatmap/
```
