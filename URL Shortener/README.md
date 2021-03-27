# URL Shortener

A small website that shortens urls. To use it, you do not need accounts or anything.<br>
Just enter the full url and you can specify your custom "Alias" to associate the url to it.

To redirect, just go to ```/url/<alias>```<br>
<br>
If Alias is not specified in the form, it will be auto generated for you!
<hr>
API Guide:<br>

 * To work with ajax requests, you need to send ```headers: {"Content-Type": "application/json"}```.
 * To create a new URL Alias, send ```POST``` request to ```/url/api``` with ```body: {"url": "your-url.com"}```. You can specify ```alias``` in the body. If not specified, it will be auto generated for you! On success, the server will return JSON containing the ```url and alias```.
