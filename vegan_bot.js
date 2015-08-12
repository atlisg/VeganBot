angular.module('VeganBotApp', ['ngRoute']);

angular.module("VeganBotApp").controller("VeganBotController", function($scope, $http) {

	$scope.justifs = {};
	$scope.answers = {};

	$http.get('justifs.json').then(function(res) {
		$scope.justifs = res.data;
	});

	$http.get('answers.json').then(function(res) {
		$scope.answers = res.data;
	});

});