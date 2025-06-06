# wikiidmon
Indonesian Wikipedia Monthly User Activity Dashboard

## How to Use
Click the username to get the details

https://github.com/altilunium/wikiidmon/assets/70379302/d74a35b5-18fd-4e06-ba5e-4eddc098bc01

## How It Works

Open the [WmCloud Superset Instance](https://superset.wmcloud.org/) to access `idwiki_p` schema at Wikimedia S2 database. Then, execute this query :

~~~sql
select actor_name, group_concat(distinct rc_title separator ';') as nya
from recentchanges join actor where rc_actor = actor_id and rc_timestamp >= 20240101000000 and rc_timestamp <= 20240201000000
group by actor_name 
~~~

> P.S. : You can configure the time window according to your own needs

After the result is generated, click "copy to clipboard", paste it to a file (all_act.txt), then convert this file into json by using this python script : 

~~~python
import sys
import json
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8')
d = dict()

with open('all_act.txt', 'r', encoding='utf-8') as file:
    line = file.readline()
    while line:
        nya = line.split("\t")
        d[nya[0]] = dict()
        d[nya[0]]["a"] = nya[1]
        d[nya[0]]["l"] = len(nya[1].split(";"))
        line = file.readline()
sorted_dict = dict(sorted(d.items(), key=lambda x: x[1]["l"], reverse=True)) 
json_data = json.dumps(sorted_dict)
print(json_data)
~~~

Finally, put this json into [a.js](https://github.com/altilunium/wikiidmon/blob/main/jan24/a.js)

#### Optional : User Collab Stat
Use this script to generate user collab stat.

~~~python
import sys
import json

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8')
d = dict()
dd = dict()

with open('all_act.txt', 'r', encoding='utf-8') as file:
    line = file.readline()
    while line:
        nya = line.split("\t")
        d[nya[0]] = dict()
        d[nya[0]]["a"] = nya[1]
        d[nya[0]]["l"] = len(nya[1].split(";"))
        line = file.readline()
        for i in nya[1].split(";"):
            if i not in dd:
                dd[i] = dict()
                dd[i]["a"] = set()
                dd[i]["a"].add(nya[0])
                dd[i]["l"] = len(dd[i]["a"])
            else:
                dd[i]["a"].add(nya[0])
                dd[i]["l"] = len(dd[i]["a"]) 

sorted_dict = dict(sorted(dd.items(), key=lambda x: x[1]["l"], reverse=True))   

for nya in sorted_dict:
    sorted_dict[nya]["a"] = list(sorted_dict[nya]["a"])

json_data = json.dumps(sorted_dict)
print(json_data)
~~~
Put this json to [b.js](https://github.com/altilunium/wikiidmon/tree/main/jan24), access it by using pco.html

#### Optional : Monthly Pageview Statistics
Get the top 1000 most visited articles from id.wikipedia for all days in specified month as JSON data:
```
https://wikimedia.org/api/rest_v1/metrics/pageviews/top/id.wikipedia/all-access/2024/01/all-days
```

Copy the JSON data, execute this python script.
~~~python
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8')
nya = PASTE_THE_JSON_DATA_HERE
rank = 1
print("== Pageview ==")
print("{| class='wikitable'")
print("!rank!!rc_title!!pageview")
print("|-")
for i in nya:
	for j in nya[i][0]["articles"]:
		strs = "|"+str(rank)+"||"+"[["+str(j["article"])+"]]||"+str(j["views"])
		print(strs)
		print("|-")
		rank = rank + 1
print("|}")
~~~

## Other queries
~~~sql
select  * /*sum(tdif)*/ 
from 
(select
actor_name,
sum( cast(rc_new_len as int) - cast(rc_old_len as int)) tdif
from recentchanges_userindex
left join actor on rc_actor = actor_id
where rc_timestamp >= 20241201000000 and rc_timestamp <= 20250101000000  and rc_bot = 0 and (rc_source = 'mw.new' or rc_source='mw.edit') 
 
 group by actor_name) a 
where tdif >= 30000
order by tdif desc
~~~

~~~sql
select *
from 
(select
rc_title,
sum( cast(rc_new_len as int) - cast(rc_old_len as int)) tdif
from recentchanges_userindex
where rc_timestamp >= 20241201000000 and rc_timestamp <= 20250101000000  and rc_bot = 0 and (rc_source = 'mw.new' or rc_source='mw.edit') 
 group by rc_title) a 
where tdif > 30000
order by tdif desc
~~~




## Compiled statistics
* January 2024
  * [User](https://altilunium.github.io/wikiidmon/jan24/)
  * [User collab](https://altilunium.github.io/wikiidmon/jan24/pco.html)
  * [Pages](https://id.wikipedia.org/wiki/Pengguna:Rtnf/Statistik_Januari_2024)
* February 2024 
  * [User](https://altilunium.github.io/wikiidmon/2024/feb/)
  * [User collab](https://altilunium.github.io/wikiidmon/2024/feb/pco.html)
  * [Pages](https://github.com/altilunium/wikiidmon/blob/main/2024/feb.txt)
* March 2024
  * [Pageread](https://github.com/altilunium/wikiidmon/blob/main/2024/mar/pageview.txt)
  * [Pagewrite](https://github.com/altilunium/wikiidmon/blob/main/2024/mar/pagewrite.txt)
  * [User](https://github.com/altilunium/wikiidmon/blob/main/2024/mar/user.txt)
* April 2024
  * [Pageread](https://github.com/altilunium/wikiidmon/blob/main/2024/apr/pageview.txt)
  * [Pagewrite](https://github.com/altilunium/wikiidmon/blob/main/2024/apr/pagewrite.txt)
  * [User](https://github.com/altilunium/wikiidmon/blob/main/2024/apr/user.txt)
* May 2024
  * [Pageread](https://github.com/altilunium/wikiidmon/blob/main/2024/mei/pageview.txt)
  * [Pagewrite](https://github.com/altilunium/wikiidmon/blob/main/2024/mei/pagewrite.txt)
  * [User](https://github.com/altilunium/wikiidmon/blob/main/2024/mei/user.txt)
* June 2024 
  * [Pageread](https://github.com/altilunium/wikiidmon/blob/main/2024/jun/read.txt)
  * [Pagewrite](https://github.com/altilunium/wikiidmon/blob/main/2024/jun/write.txt)
  * [User](https://github.com/altilunium/wikiidmon/blob/main/2024/jun/user.txt)
* July 2024
  * [Pageread](https://github.com/altilunium/wikiidmon/blob/main/2024/jul/view.txt)
  * [Pagewrite](https://github.com/altilunium/wikiidmon/blob/main/2024/jul/page.txt)
  * [User](https://github.com/altilunium/wikiidmon/blob/main/2024/jul/user.txt)
* August 2024 : [Write](https://github.com/altilunium/wikiidmon/blob/main/2024/aug/write.txt), [Read](https://github.com/altilunium/wikiidmon/blob/main/2024/aug/read.txt), [User](https://github.com/altilunium/wikiidmon/blob/main/2024/aug/user.txt)
