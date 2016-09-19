/**
 * Created by sam on 9/12/16.
 */
(function text_field_ed(value) {
    var values = [
        'public', 'subsets', 'uplines', 'directs',
        'upline', 'private'
    ];
    switch (value) {
        case values[0]:
            var elem1 = document.getElementById("ilk_publication");
            elem1.setAttribute("disabled", "enable");
            break;

        case values[1]:
            var elem2 = document.getElementById("ilk_publication");
            elem2.setAttribute("disabled", "enable");
            break;

        case values[2]:
            var elem3 = document.getElementById("ilk_publication");
            elem3.setAttribute("disabled", "enable");
            break;

        case values[3]:
            var elem4 = document.getElementById("ilk_publication");
            elem4.setAttribute("disabled", "enable");
            break;

        case values[4]:
            var elem5 = document.getElementById("ilk_publication");
            elem5.setAttribute("disabled", "enable");
            break;

        case values[5]:
            var elem6 = document.getElementById("ilk_publication");
            elem6.setAttribute("disabled", "enable");
            break;
    }
});
