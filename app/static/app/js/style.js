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
<script type="text/javascript">
    $(function(){
    // #で始まるアンカーをクリックした場合に処理
    $('a[href^=#]').click(function() {
        // スクロールの速度
        var speed = 400; // ミリ秒
        // アンカーの値取得
        var href= $(this).attr("href");
        // 移動先を取得
        var target = $(href == "#" || href == "" ? 'html' : href);
        // 移動先を数値で取得
        var position = target.offset().top;
        // スムーススクロール
        $('body,html').animate({scrollTop:position}, speed, 'swing');
        return false;
    });
    });
</script>