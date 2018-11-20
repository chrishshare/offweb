$(function () {
// menuList();
bannerList('.home-ind', '.home-inner');
    footerList();
});

function menuList() {
    $.ajax({
        type: 'post',
        url: '/menu/',
        success:function (data) {
            $.each(JSON.parse(data), function (index, content) {
                createMenu(content);
            })
        }
    })
}


function createMenu(content) {
    let menuroot = $('.menu');
    for (let i = 0; i < content.body.length; i++){
        let menuli = $('<li></li>');
        menuroot.append(menuli);
        let menua = $('<a></a>');
        menua.attr("href", "#");
        menua.text(content.body[i].menuname);
        menuli.append(menua)
    }
}


function bannerList(ind, inner) {
    $.ajax({
        type: 'post',
        url: '/banner/',
        success:function (data) {
            $.each(JSON.parse(data), function (index, content) {
                createBanner(ind, inner, content);
            })
        }
    })
}



function createBanner(ind, inner, content) {
    //创建元素，传入ind：操作顺序的class， inner：图片的class
    bodyLength = content.body.length;
    console.log(bodyLength);
    for (let i = 0; i < bodyLength; i++){
        //添加元素到<ol class="carousel-indicators">
        let ind_li = $('<li data-target="#carousel"></li>');
        let inner_item = $('<div class="item"></div>')
        if (i === 0) {
            ind_li.attr("class", "active");
            // inner_item.attr("class", "active");
            inner_item.addClass("active");
        }
        inner_item.css("background", content.body[i].fill);
        ind_li.attr("data-slide-to", i);
        $(ind).append(ind_li);
        $(inner).append(inner_item);


        let img_a = $('<a target="_blank"></a>');
        img_a.attr("href", content.body[i].linkaddr);
        $(inner_item).append(img_a);

        let item_img = $('<img>');
        item_img.attr("src", "/media/" + content.body[i].imgsrc);
        item_img.attr("alt", content.body[i].mediainfo);

        let item_div = $('<div class="carousel-caption"></div>');
        item_div.text(content.body[i].mediainfo);
        $(img_a).append(item_img);
        $(inner_item).append(item_div);

        let let_ctl = $('<a class="left carousel-control" href="#carousel" role="button" data-slide="prev"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span><span class="sr-only">Previouse</span></a>');
        let right_ctl = $('<a class="right carousel-control" href="#carousel" role="button" data-slide="next"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span><span class="sr-only">next</span></a>');

        $('.carousel-inner').append(let_ctl);
        $('.carousel-inner').append(right_ctl);
    }
}


function createPodBanner(ind, inner, content) {

}

function footerList() {
 $.ajax({
        type: 'post',
        url: '/menu/',
        success:function (data) {
            $.each(JSON.parse(data), function (index, content) {
                console.log(content);
                createFooter(content)
            })
        }
 })
}


function createFooter(content){
     let bodyLength = content.body.length;
     for(let i=0;i<bodyLength;i++){
         let outerdiv = $('<div class="col-lg-2 col-md-4 col-sm-6 footdiv"></div>');
         $('.footer-menu').append(outerdiv);
         let vh2 = $('<h2></h2>');
         vh2.text(content.body[i].menuname);
         $(outerdiv).append(vh2);
         let vhr = $('<hr>');
         $(outerdiv).append(vhr);
         let vul = $('<ul></ul>');
         $('.footdiv').append(vul);
         for(let j = 0; j< content.body[i].childmenu.length; j++){
             let vli = $('<li></li>')
             $(vli).text(content.body[i].childmenu[j].menuname)
             $(vul).append(vli)
         }
     }

}


function backtop() {
    window.scrollBy(0,-10);
    scrolldelay=setTimeout('pageScroll()',100);
    if(document.documentElement.scrollTop==0){
        clearTimeout(scrolldelay)
    };
}

