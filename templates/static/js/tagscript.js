function change_display(repo_name) {
    var div_tag = document.getElementById('div-tag-' + repo_name);
    var div_input_tag = document.getElementById('div-input-tag-' + repo_name);
    if (div_tag.style.display != 'none') {
        div_tag.style.display = 'none';
        div_input_tag.style.display = 'block';
    } else {
        div_tag.style.display = 'block';
        div_input_tag.style.display = 'none';
    }
}
