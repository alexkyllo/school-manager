'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('userSchoolsCtrl', function($scope, api, Shared){
    $scope.Shared = Shared;
    $scope.schools = api.schools.get(function(data){
            return data.schools;
        });
  })
  .controller('CalendarCtrl', ['$scope', 'api', 'Shared', function($scope, api, Shared) {
    $scope.Shared = Shared;
    $scope.initializeCalendar = function(){
        $scope.uiConfig = {
        calendar : {
          height: 450,
          editable: true,
          header:{
            left: 'month agendaWeek agendaDay',
            center: 'title',
            right: 'today prev,next'
          }
        }
      }
      $scope.eventSource = {
          url: "/events/",
          timezone: "UTC",
          data: {
            schoolId: Shared.selectedSchool.id
          }
        }
      $scope.eventSources = []
      $scope.eventSources.push($scope.eventSource);
      $scope.$watch('Shared.selectedSchool', function() {
        $scope.refetchEvents();
      });
      $scope.refetchEvents = function(){
        var newEventSource = {
          url: "/events/",
          timezone: "UTC",
          data: {
            schoolId: Shared.selectedSchool.id
          }
        }
        $scope.eventSources.push(newEventSource);
        $scope.eventSources.shift();
      }
    }
    var unbindWatcher = $scope.$watch('Shared.selectedSchool', function(){
      if (Shared.selectedSchool != undefined){
        $scope.initializeCalendar();
        unbindWatcher();
      }
    })

  }])
  .controller('StudentListCtrl', function($scope, api, Shared) {
      $scope.Shared = Shared;
      $scope.getStudents = function(){
        api.schoolStudents.get({schoolId : Shared.selectedSchool.id}).
        $promise.then(
          function(data){
            $scope.students = data;
          }
        )
      }
      $scope.$watch('Shared.selectedSchool', function() {
        $scope.getStudents();
      });
  })
  .controller('CourseListCtrl', function($scope, api, Shared) {
      $scope.Shared = Shared;
      $scope.getCourses = function(){
        api.schoolCourses.get({schoolId : Shared.selectedSchool.id}).
        $promise.then(
          function(data){
            $scope.courses = data;
          }
        )
      }
      $scope.$watch('Shared.selectedSchool', function() {
        $scope.getCourses();
      });
  })
  .controller('authController', function($scope, api, authState, Shared) {
        
        //$('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.authState = authState;
        $scope.Shared = Shared;

        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
        $scope.login = function(){
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        authState.user = data.username;
                    }).
                    catch(function(data){
                        alert(data.data.detail);
                    });
        };
        $scope.logout = function(){
            api.auth.logout(function(){
                authState.user = undefined;
            });
        };
        $scope.register = function($event){
            $event.preventDefault();
            api.users.create($scope.getCredentials()).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
        };
    });
