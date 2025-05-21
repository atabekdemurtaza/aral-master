from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse


# Функция для отображения простой API документации
def api_docs_view(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GreenAralSea API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            h2 {
                color: #3498db;
                margin-top: 30px;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin-bottom: 10px;
            }
            a {
                color: #2980b9;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .endpoint {
                background-color: #f9f9f9;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 5px;
            }
            .method {
                display: inline-block;
                padding: 3px 6px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get {
                background-color: #61affe;
                color: white;
            }
            .post {
                background-color: #49cc90;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GreenAralSea API Documentation</h1>

            <p>This is the API documentation for GreenAralSea.org website. Below are the available endpoints:</p>

            <h2>News Endpoints</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/news/list/">/api/v1/news/list/</a> - Get a list of all published news
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/news/list/?lang=en">/api/v1/news/list/?lang=en</a> - Get news in English (also available: lang=ru, lang=uz)
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/news/detail/1/">/api/v1/news/detail/{id}/</a> - Get details for a specific news item
            </div>

            <h2>Donation Endpoints</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/donation/total/">/api/v1/donation/total/</a> - Get total donation amount
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/donation/list/most/recent/">/api/v1/donation/list/most/recent/</a> - Get most recent donations
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/donation/list/most/amount/">/api/v1/donation/list/most/amount/</a> - Get donations ordered by amount
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <span>/api/v1/donation/create/</span> - Create a new donation
            </div>

            <h2>Other Endpoints</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/ambassador/list/">/api/v1/ambassador/list/</a> - Get list of ambassadors
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/team-member/list/">/api/v1/team-member/list/</a> - Get list of team members
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/partner/list/">/api/v1/partner/list/</a> - Get list of partners
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/green-champion/list/">/api/v1/green-champion/list/</a> - Get list of green champions
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/youtube-link/list/">/api/v1/youtube-link/list/</a> - Get list of YouTube links
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/faq/list/">/api/v1/faq/list/</a> - Get list of FAQs
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <a href="/api/v1/learn-more/list/">/api/v1/learn-more/list/</a> - Get list of learn more entries
            </div>

            <h2>Admin Interface</h2>
            <p>Go to the <a href="/admin/">Admin Interface</a> to manage content.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


urlpatterns = [
                  # API документация
                  path('', api_docs_view, name='api-docs'),

                  # Оригинальные URLs
                  path('api/v1/', include('api.urls'), name='api'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('tinymce/', include('tinymce.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)