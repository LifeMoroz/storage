function remove_from_favorites() {
    var parent = $(this).parent().parent().parent();
    parent.parent().append("<div class=\"col-12\"><br /><h4>Вы ещё не делали закладок.</h4></div>");
    parent.remove();
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