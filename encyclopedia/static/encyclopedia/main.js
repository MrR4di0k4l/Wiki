let abc_form = document.getElementById('alphabet_form')
document.querySelectorAll('.link_anchor').forEach(function (btn) {

    btn.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById("abc_input").value = btn.dataset.value;

        let spinner = document.getElementById('spinner');
        setTimeout(function () {
            spinner.classList.remove('invisible');
        }, 1000)
        abc_form.submit();
    })
})
