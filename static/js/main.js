function remove_from_favorites() {
    var parent = $(this).parent().parent().parent();
    var container = parent.parent();
    parent.remove();
    if ($('.card').length == 0) {
        container.append("<div class=\"col-12\"><br /><h4>Вы ещё не делали закладок.</h4></div>");
    }
}

function toggle_favorite(_this) {
    var parent = $(_this).parent();
    var addEl = parent.children('.favorites-add');
    var removeEl = parent.children('.favorites-remove');
    if (addEl.is(':visible')) {
      addEl.hide();
      removeEl.show();
    }
    else {
      removeEl.hide();
      addEl.show();
    }
}