$(document).ready(function() {
    // edit item
    $(".edit-btn").on('click', function () {
      var itemId = this.id;
      $("#item" + itemId).hide();
      $("#form" + itemId).show();
      $(".cancel-btn").click(function() {
          $("#form" + itemId).hide();
          $("#item" + itemId).show();
      });
    });

    //$('.items').sortable({ handle: '.move' });
    $('select').material_select();
    $(".button-collapse").sideNav();

    // add new item
    $("#new-item").click(function() {
        if ($("#category-select").val() == null) {
            Materialize.toast('分类还没选呢~', 4000)
        } else if ($("#item-input").val() == '') {
            Materialize.toast('你的todo是空的！', 4000)
        } else if (parseInt($("#items-count").html(), 10) >= 15) {
            Materialize.toast('Sorry，条目太多了，删掉几个吧。', 3000);
        } else {
            Materialize.toast('todo添加成功！', 3000, 'rounded');
            document.getElementById('add-item-form').submit()
        }
    });

    $("#new-category").click(function() {
        if ($("#category-input").val() == '') {
            Materialize.toast('你什么都没有填呢~', 4000)
        } else if (parseInt($("#category-count").html(), 10) >= 12) {
            Materialize.toast('Sorry，分类太多了，删掉几个吧。', 3000);
        } else {
            Materialize.toast('分类添加成功！', 3000, 'rounded');
            document.getElementById('add-category-form').submit()
        }
    });



    $(".item-done").click(function() {
        $(this).parent().slideUp();
        Materialize.toast('Well Done +1', 3000, 'rounded')
    });

    $(".categories").hover(function() {
        $(this).find(".delete-category").show();
        }, function() {$(this).find(".delete-category").hide()
    });

    $(".confirm-btn").click(function() {
        Materialize.toast('修改成功~', 3000, 'rounded')
    });

    $(".delete-item").click(function() {
        $(this).parent().slideUp();
        Materialize.toast('删除成功~', 3000, 'rounded')
    });

    $(".delete-category").click(function() {
        $(this).parent().slideUp();
        Materialize.toast('删除成功~', 3000, 'rounded')
    });

    $(".signin").click(function() {
        Materialize.toast('暂未添加用户系统，抱歉~', 3000)
    });
})








