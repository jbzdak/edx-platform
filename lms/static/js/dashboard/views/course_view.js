;(function (define) {
    'use strict';

    define(['jquery', 'backbone', 'underscore', 'logger'],
        function ($, Backbone, _, Logger) {
            var CourseView = Backbone.View.extend({

                events: {
                    'click .action-more': 'toggleCourseActionsDropdown',
                    'click .action-unenroll': 'unEnroll',
                    'click .action-email-settings': 'emailSettings',
                    'click #upgrade-to-verified': 'upgradeToVerified',
                    'click #block-course-msg a[rel="leanModal"]': 'unRegisterBlockCourse'
                },

                initialize: function (options) {
                    this.setElement(this.el);
                    this.listenTo(options.tabbedView, 'rendered', this.rendered);
                },

                rendered: function () {
                    var $actionUnroll = this.$('.action-unenroll');
                    var $unRegisterBlockCourse = this.$('#unregister_block_course');

                    this.bindUnEnrollModal($actionUnroll);
                    this.bindUnEnrollModal($unRegisterBlockCourse);
                    this.bindEmailSettingsModal();
                },

                bindUnEnrollModal: function ($selector) {
                    $selector.leanModal({
                        overlay: 1,
                        closeButton: ".close-modal"
                    });

                    var id = _.uniqueId('unenroll-');
                    $selector.attr('id', id);
                    var trigger = "#" + id;

                    accessible_modal(
                        trigger,
                        "#unenroll-modal .close-modal",
                        "#unenroll-modal",
                        "#dashboard-main"
                    );
                },

                bindEmailSettingsModal: function () {
                    var $actionEmailSettings = this.$('.action-email-settings');

                    $actionEmailSettings.leanModal({
                        overlay: 1,
                        closeButton: ".close-modal"
                    });

                    var id = _.uniqueId('email-settings-');
                    $actionEmailSettings.attr('id', id);
                    var trigger = "#" + id;

                    accessible_modal(
                        trigger,
                        "#email-settings-modal .close-modal",
                        "#email-settings-modal",
                        "#dashboard-main"
                    );
                },

                toggleCourseActionsDropdown: function (e) {
                    var index = this.$(e.currentTarget).data('dashboard-index');

                    // Toggle the visibility control for the selected element and set the focus
                    var $dropDown = this.$('div#actions-dropdown-' + index);

                    $dropDown.toggleClass('is-visible');
                    if ($dropDown.hasClass('is-visible')) {
                        $dropDown.attr('tabindex', -1);
                    } else {
                        $dropDown.removeAttr('tabindex');
                    }

                    // Inform the ARIA framework that the dropdown has been expanded
                    var anchor = this.$(e.currentTarget);
                    var ariaExpandedState = (anchor.attr('aria-expanded') === 'true');
                    anchor.attr('aria-expanded', !ariaExpandedState);

                    // Suppress the actual click event from the browser
                    e.preventDefault();
                },

                unEnroll: function (e) {

                    var $selector = this.$(e.currentTarget);
                    var track_info = $selector.data("track-info");
                    var courseId = $selector.data("course-id");
                    var courseNumber = $selector.data("course-number");
                    var courseName = $selector.data("course-name");
                    var certNameLang = $selector.data("cert-name-long");
                    var refundInfo = $selector.data("refund-info");

                    $('#track-info').html(interpolate(track_info, {
                        course_number: "<span id='unenroll_course_number'>" + courseNumber + "</span>",
                        course_name: "<span id='unenroll_course_name'>" + courseName + "</span>",
                        cert_name_long: "<span id='unenroll_cert_name'>" + certNameLang + "</span>"
                    }, true));

                    $('#refund-info').html(refundInfo);
                    $("#unenroll_course_id").val(courseId);
                },

                emailSettings: function (e) {
                    $("#email_settings_course_id").val(this.$(e.currentTarget).data("course-id"));
                    $("#email_settings_course_number").text(this.$(e.currentTarget).data("course-number"));

                    if (this.$(e.currentTarget).data("optout") === "False") {
                        $("#receive_emails").prop('checked', true);
                    }
                },

                upgradeToVerified: function (e) {
                    var user = this.$(e.currentTarget).closest(".action-upgrade").data("user");
                    var course = this.$(e.currentTarget).closest(".action-upgrade").data("course-id");

                    Logger.log('edx.course.enrollment.upgrade.clicked', [user, course], null);
                },

                unRegisterBlockCourse: function (e) {
                    if (this.$('#block-course-msg').length) {
                        $('.disable-look-unregister').click();
                    }

                    var $selector = this.$(e.currentTarget);

                    var courseId = $selector.data("course-id");
                    var courseNumber = $selector.data("course-number");
                    var courseName = $selector.data("course-name");

                    $('#track-info').html("<span id='unenroll_course_number'>" + courseNumber + "</span>" +
                        " - <span id='unenroll_course_name'>" + courseName + "?</span>");

                    $("#unenroll_course_id").val(courseId);
                }
            });

            return CourseView;
        });

}).call(this, define || RequireJS.define);
