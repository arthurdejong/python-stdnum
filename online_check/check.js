/*
 # check.js - simple application to check numbers
 #
 # Copyright (C) 2017 Arthur de Jong.
 #
 # This library is free software; you can redistribute it and/or
 # modify it under the terms of the GNU Lesser General Public
 # License as published by the Free Software Foundation; either
 # version 2.1 of the License, or (at your option) any later version.
 #
 # This library is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this library; if not, write to the Free Software
 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 # 02110-1301 USA
 */

$( document ).ready(function() {

  function format(value) {
    return $("<div/>").text(value).html().replace(
      /\n\n/g, "<br/>\n"
    ).replace(
      /^[*] (.*)$/gm, "<ul><li>$1</li></ul>"
    ).replace(
      /(\b(https?|ftp):\/\/[^\s<]*[-\w+&@#/%=~_|])/ig,
      "<a href='$1'>$1</a>"
    )
  }

  function updateresults(field, results) {
    // build HTML to present
    var h = ["<ul>"];
    $.each(results, function(index, result) {
      h.push(
        "<li><b>",
        $("<div/>").text(result["name"]).html(),
        "</b><br/>",
        $("<div/>").text(result["number"]).html(),
        "<p>",
        format(result["description"]),
        $.map(result["conversions"], function(value, key){
          return [
            "<br/><b><i>",
            $("<div/>").text(key).html(),
            "</i></b>: ",
            $("<div/>").text(value).html()].join('')
        }).join(''),
        "</p></li>")
    });
    h.push("</ul>");
    // replace the results div
    $("#" + $(field).attr("id") + "_results").slideUp("quick", function() {
      $(this).html(h.join(""));
      $(this).slideDown("quick");
    });
  }

  function checkfield(field) {
    var value = field.val();
    // only trigger update if value changed from previous validation
    if (value != $(this).data("oldvalue")) {
      $(this).data("oldvalue", value);
      $.get('', {number: value}, function(data) {
        updateresults(field, data);
      });
    }
  }

  // trigger a check when user stopped typing
  $(".stdnum_check").on("input propertychange", function (event) {
      if (window.event && event.type == "propertychange" && event.propertyName != "value")
        return;
      var field = $(this);
      window.clearTimeout($(this).data("timeout"));
      $(this).data("timeout", setTimeout(function () {
        checkfield(field);
    }, 2000));
  });

  // trigger a check when losing focus
  $(".stdnum_check").on("blur", function() {
    window.clearTimeout($(this).data("timeout"));
    checkfield($(this));
  });

  // prevent enter from submitting the form
  $(".stdnum_check").keydown(function(event) {
    if(event.keyCode == 13) {
      event.preventDefault();
      checkfield($(this));
      return false;
    }
  });

  // hide the submit button
  $(".stdnum_hide").hide();

  // focus the text field
  $(".stdnum_check").focus();

});
