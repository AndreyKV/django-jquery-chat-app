$('#chat-form').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url: "/send_message/" + window.location.search,
        type: "POST",
        data: {
            csrfmiddlewaretoken : csrftoken,
            msg_text: $("#msg-text").val()
        },

        success: function(json) {
            $('#msg-text').val("");
            $('#msg-list').append(
                '<li><p><span class="username">' + json["sender"] +
                '</span><span class="message-date">' + json["date"] +
                '</span></p><p>' + json["msg"] + '</p></li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});

function getMessages(){
    if (!scrolling) {
        $.get('/messages/'+window.location.search, function(messages){
            $('#msg-list').html(messages);
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 500);
});

function getDialogs(){
    if (!scrolling) {
        $.get('/dialogs/', function(dialogs){
            $('#dialog-list').html(dialogs);
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#dialogs-list-div').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getDialogs, 500);
});

$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#msg-text').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
});

$(function() {

    $('#search').keyup(function() {

        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                csrfmiddlewaretoken : csrftoken,
                search_text: $('#search').val(),
            },
            success: searchUser,
            dataType: 'html'
        });
    });
});

function searchUser(data, textStatus, jqXHR)
{
    $('#search-result').html(data);
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
