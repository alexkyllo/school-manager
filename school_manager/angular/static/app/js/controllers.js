'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
  .controller('userSchoolsCtrl', function($scope, api, Shared){
    $scope.Shared = Shared;
    $scope.schools = api.schools.get(function(data){
            return data.schools;
        });
  })
  .controller('CalendarCtrl', ['$scope', 'api', '$modal', 'Shared', function($scope, api, $modal, Shared) {
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

    $scope.openModal = function(){
      $modal.open({templateUrl:'../static/app/partials/new_event.html'});
    }

  }])
  .controller('StudentListCtrl', ['$scope', '$modal', 'api', 'Shared', function($scope, $modal, api, Shared) {
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
      $scope.openModal = function(student, size, method){
        $scope.method = method;
        $scope.student = student;
        var modalInstance = $modal.open({
          templateUrl: '../static/app/partials/student_details.html',
          controller: function($scope, $modalInstance, student, api, method){
              $scope.method = method;
              console.log("Method: " + $scope.method);
              $scope.student = student;
              if ($scope.method == 'new'){
                $scope.editing = true;
              } else {
                $scope.editing = false;
              }
              $scope.setEditing = function(){
                $scope.editing = true;
              }
              $scope.setStudent = function(student){
                $scope.student = student;
              }
              $scope.ok = function () {
                $modalInstance.close($scope.student);
              };

              $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
              };

            },
          size: size,
          resolve: {
            student: function(){
              return $scope.student;
            },
            method: function(){
              return $scope.method;
            }
          }
        })
        modalInstance.result.then(function(student){
          console.log("modal closed");
          $scope.getStudents();
        });
      }
  }])
  .controller('StudentEditCtrl', ['$scope','api', function($scope, api){
    if ($scope.student){
      $scope.user = angular.copy($scope.student);
    } else {
      $scope.user = new api.students();
    }
    $scope.saveUser = function() {
      if ($scope.student){
        api.users.update($scope.user, function(result){
          $scope.setStudent(angular.copy($scope.user));
        });
      } else {
        $scope.user.save().$promise.then(
          function(result){
          $scope.setStudent(angular.copy($scope.user));
        })
      }
    }
  }])
  .controller('CourseListCtrl', ['$scope', '$modal', 'api', 'Shared', function($scope, $modal, api, Shared) {
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
  }])
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
