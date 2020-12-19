// /* acordion */
// $(".accordion-wrap").on("click", function(){   
//     $(this).children().eq(1).slideToggle(300);  
//     $(this).children().eq(0).toggleClass("accordion-no-bar");
//     $(this).siblings().find(".accordion-header").removeClass("accordion-gold");
//     $(this).siblings().find(".accordion-header i").removeClass("rotate-fa");
//     $(this).find(".accordion-header").toggleClass("accordion-gold");
//     $(this).find(".fa").toggleClass("rotate-fa");

//     $(".accordion-wrap .accordion-text").not($(this).children().eq(1)).slideUp(300);
// });

// $(function(){
//     $('.js-menu__item__link').each(function(){
//         $(this).on('click',function(){
//             $("+.submenu",this).slideToggle();
//             return false;
//         });
//     });
// }); 

// スムーズスクロール部分の記述
$(function() {
    var headerHeight = $('.sticky-top').outerHeight();
    var urlHash = location.hash;
    if(urlHash) {
        $('body,html').stop().scrollTop(0);
        setTimeout(function(){
            var target = $(urlHash);
            var position = target.offset().top - headerHeight;
            $('body,html').stop().animate({scrollTop:position}, 500);
        }, 100);
    }
    console.log('bbb')
  // ①aタグをクリックし、href属性に # から始まるリンクが設定してあったら発動
  $('a[href^="/#"]').click(function(){
 
    // ②クリックしたaタグのhref属性（リンク先URI）を取得し、変数に格納
    var href = $(this).attr('href');
    console.log(href)

    // ③上で取得した値が#か空白だったら'html'を、それ以外だったら先ほど取得したhref属性の値を変数に格納
    var target = $(href)
    // href == '#' || href === '' ? 'html' : href);
 
    // ④変数targetのページトップからの位置を取得し、変数に格納
    var position = target.offset().top;
    console.log('aaa')
 
    // ⑤scrollTopに上で取得した位置を設定し、ヌルヌルとスクロールさせる
    $('html,body').animate({scrollTop : position}, 500);
 
    // ⑥a要素のデフォルトの機能を無効化する
    return false;
 
  });
});