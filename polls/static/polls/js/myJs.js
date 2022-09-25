
// var formData = {
//     name: '',
//     paw: '',
//     age: '',
// }


// $(document).ready(function() {
//     alert('Hi');
//     var result = confirm('Check');
//     alert(result);
//     $('input').on('input', function () {
//         var name = $(this).data('name');
//         var oldValue = formData[name];
//         var newValue = $(this).val();
//         // alert(newValue);
//         formData[name] = newValue;
//         if (!(oldValue && newValue)) { //1.之前无值现在有值 2.之前有值现在删除了
//             $('#save_btn').attr("disabled", isFormReady());
//         }
//     })
// })
//
// function isFormReady() {
//     for (let i in formData) {
//         if (!formData[i]) return true
//     }
//     return false
// }

// ------------ Form for Programme Judge page ------------



$(document).ready(function() {

    // ------------ Form for Programme (Regular) Judge page ------------

    var progJudgeForm = {};
    var progJudgePosterNumber = Number($('#num_poster_programme').text());

    $('.my-programme-input').on('input', function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        if (value.length !== 0) {
            // alert('Yes');
            progJudgeForm[name] = value;
        } else {
            // alert('NO');
            progJudgeForm[name] = 0;
        }
        if (Object.keys(progJudgeForm).length === progJudgePosterNumber) {
            var prog_judge_finish = 1;
            $.each(progJudgeForm, function (k, v) {
                if (v === 0) {
                    prog_judge_finish = 0;
                }
            })
            if (prog_judge_finish === 1) {
                // Active the button
                $('#programme_judge_button').attr("disabled", false);
            } else {
                $('#programme_judge_button').attr("disabled", true);
            }
        }
    })

    $('#programmeForm').submit( function () {
        var confirm_text = "Dear Judge,\nThis is your rate record:\n";
        $.each(progJudgeForm, function (k, v) {
            confirm_text += String(k) + ': ' + String(v) + '\n';
        })
        confirm_text += "Confirm submission?";
        return confirm(confirm_text);
    })

    // ------------ Form for Head Judge page ------------

    var headJudgeForm = {};
    var headJudgePosterNumber = Number($('#num_poster_division').text());

    $('.my-division-input').on('input', function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        if (value.length !== 0) {
            // alert('Yes');
            headJudgeForm[name] = value;
        } else {
            // alert('NO');
            headJudgeForm[name] = 0;
        }
        if (Object.keys(headJudgeForm).length === headJudgePosterNumber) {
            var head_judge_finish = 1;
            $.each(headJudgeForm, function (k, v) {
                if (v === 0) {
                    head_judge_finish = 0;
                }
            })
            if (head_judge_finish === 1) {
                // Active the button
                $('#head_judge_button').attr("disabled", false);
            } else {
                $('#head_judge_button').attr("disabled", true);
            }
        }
    })

    $('#divisionForm').submit( function () {
        var confirm_text = "Dear Judge,\nThis is your rate record:\n";
        $.each(headJudgeForm, function (k, v) {
            confirm_text += String(k) + ': ' + String(v) + '\n';
        })
        confirm_text += "Confirm submission?";
        return confirm(confirm_text);
    })

    // ------------ Form for Coordinator page ------------

    var coordinatorForm = {
        'title': 0,
        'author': 0,
        'division': 0,
        'programme': 0,
        'abstract': 0,
    };

    $('.coordinator-input').on('input', function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        if (value.length !== 0) {
            coordinatorForm[name] = 1;
            if (isFormReady(coordinatorForm)) {
                var fileInput = $('#coordinator_file').get(0).files[0];
                if (fileInput) {
                    $('#coordinator_button').attr("disabled", false);
                } else {
                    $('#coordinator_button').attr("disabled", true);
                }
            } else {
                $('#coordinator_button').attr("disabled", true);
            }
        } else {
            coordinatorForm[name] = 0;
            $('#coordinator_button').attr("disabled", true);
        }
    })

    $('#coordinator_form').submit( function () {
        return confirm("Are you sure?");
    })

    // ------------ Form for Admin page ------------

    var adminForm = {
        'name': 0,
        'abstract': 0,
        'regular_judge': 0,
        'head_judge': 0,
        'first_prize': 0,
        'second_prize': 0,
        'third_prize': 0,
    };

    $('.admin-input').on('input', function () {
        var name = $(this).attr('name');
        var value = $(this).val();
        if (value.length !== 0) {
            adminForm[name] = 1;
            if (isFormReady(adminForm)) {
                $('#admin_button').attr("disabled", false);
            } else {
                $('#admin_button').attr("disabled", true);
            }
        } else {
            adminForm[name] = 0;
            $('#admin_button').attr("disabled", true);
        }
    })

    $('#admin_form').submit( function () {
        var check_info = prompt("Create this conference will change the database,\n" +
            "It may cause information loss of some staff.\n" +
            "Please input 'Admin check' to confirm this creation:");
        return check_info === 'Admin check';
    })

    // ------------ Form for chairman page ------------

    $('#lucky_draw_form').submit( function () {
        var check_info = prompt("Lucky draw will begin soon,\n" +
            "Please input 'Chairman check' to confirm this creation:");
        if (check_info === 'Chairman check') {
            $('#lucky_draw_button').attr("disabled", true);
            alert('Lucky draw starting!\nAll email have sent!\nYour can logout now.')
            return true;
        } else {
            return false;
        }
    })

    $('#lucky_draw_unlock').click(function () {
        $('#lucky_draw_button').attr("disabled", false);
    })

    // ------------ Form for update page ------------

    $('#edit_form').submit( function () {
        return confirm("Are you sure?");
    })

})

function isFormReady(form) {
    var ret = true;
    $.each(form, function (k, v) {
        if (v === 0) {
            ret = false;
        }
    })
    return ret;
}
