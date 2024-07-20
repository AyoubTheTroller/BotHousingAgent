## Show full lines logs with Systemctl

```bash
sudo systemctl status bothousingagent.service --no-pager -l
```

```bash
sudo systemctl status servicename -n 1000
```

## Show full lines logs with Journalctl

```bash
sudo journalctl -u bothousingagent.service --no-pager

```