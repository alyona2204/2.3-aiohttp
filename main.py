from aiohttp import web
import sqlite3
DB_NAME = 'ads.db'


app = web.Application()

async def add_ad(request):
    data = await request.post()
    title = data.get('title')
    description = data.get('description')
    owner = data.get('owner')

    conn = sqlite3.connect('ads.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ads (title, description, owner) VALUES (?,?,?)", (title, description, owner))
    conn.commit()
    conn.close()

    return web.Response(text="Ad created successfuly")

async def get_ad(request):
    ad_id = request.match_info.get('id')

    conn = sqlite3.connect('ads.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ads WHERE id=?', ad_id)
    result = cursor.fetchone()
    if result:
        ad_dict = {
            'id': result[0],
            'title': result[1],
            'description': result[2],
            'owner': result[3],
            'created_date': result[4]
        }
        return web.json_response(ad_dict)
    else:
        return web.Response(text='Ad not found', status=404)


async def delete_ad(request):
    ad_id = request.match_info.get('id')

    conn = sqlite3.connect('ads.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ads WHERE id=?', ad_id)
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM ads WHERE id=?", ad_id)
        conn.commit()
        conn.close()
        return web.Response(text='Ad deleted successfuly')
    else:
        return web.Response(text='Ad not found', status=404)

app.router.add_post('/ads', add_ad)
app.router.add_get('/ads/{id}', get_ad)
app.router.add_delete('/ads/{id}', delete_ad)

if __name__ == '__main__':
    web.run_app(app)