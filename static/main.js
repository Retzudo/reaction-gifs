(function() {
    "use strict";

    var app = angular.module('GifsApp', ['angularLazyImg']);

    app.controller('GifsController', ['$rootScope', '$scope', '$http', function($rootScope, $scope, $http) {
        $scope.gifs = [];
        $scope.search = '';

        $http.get('/gifs.json').then(function (response) {
            $scope.gifs = response.data.gifs;
        });

        $scope.lazyLoad = function () {
            $rootScope.$emit('lazyImg:refresh');
        }
    }]);
}());
