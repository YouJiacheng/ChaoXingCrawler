// ==UserScript==
// @name         Download
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http://*/*
// @grant        GM_download
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict'
    GM_addStyle(`
    #download{
      position: fixed;
      top: 10px;
      right:10px;
      z-index: 99999;
      background: gray;
    }
    #download_trigger{
        text-align: center;
    }
    #download_trigger:hover{
        background: green;
    }
    `)

    let elem = document.createElement('div')
    elem.id = 'download'
    elem.innerHTML = `
    <div id="download_trigger">下载</div>
    <div>起始页<input id="download_begin" type="number"></div>
    <div>结束页<input id="download_end" type="number"></div>
    `
    document.body.appendChild(elem)
    document.getElementById('download_trigger').addEventListener('click', () => {
        const imgs_src = Array.prototype.map.call(document.getElementsByClassName('readerImg'), img => img.src)
        const reducer = (a, b) => a.length > b.length ? a : b
        const real_src = Array.prototype.reduce.call(imgs_src, reducer)
        const base = real_src.split('/').slice(0, -1).join('/')
        const begin = Number(document.getElementById('download_begin').value)
        const end = Number(document.getElementById('download_end').value)
        for (let page = begin; page <= end; ++page)
        {
            const page_str = String(page)
            const num_w = page_str.length
            const page_str_formatted = '0'.repeat(6 - num_w) + page_str
            const download_url = `${base}/${page_str_formatted}?zoom=2`
            console.log(download_url)
            GM_download(download_url, `${page}`)
        }
        
    })
})();