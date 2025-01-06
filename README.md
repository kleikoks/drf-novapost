settings.py file:
```
NP_API_KEY=YOUR_API_KEY
```

Simply run management command
```shell
python manage.py nova_post
```

or use cron
```shell
sudo ln -s ./.../nova_post_name /etc/cron.d/nova_post_name
sudo chmod 0744 ./nova_post_name
```