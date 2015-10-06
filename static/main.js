(function() {
    var app = angular.module('GifsApp', []);

    app.config(['$sceDelegateProvider', function ($sceDelegateProvider) {
        $sceDelegateProvider.resourceUrlWhitelist([
            'self',
            'http://zippy.gfycat.com/**'
        ]);
    }]);

    app.controller('GifsController', ['$scope', '$http', function($scope, $http) {
        $scope.gifRows = [];
        $scope.search = '';

        var allGifs = [];

        $http.get('/gifs')
            .then(function(data) {
                allGifs = _.map(data.data.gifs, function (gif) {
                    if (gif.gfycat && gif.gfycat.length > 0) {
                        gif.webm = getWebmUrl(gif.gfycat);
                        gif.mp4 = getMp4Url(gif.gfycat);
                    }
                    return gif;
                });
                $scope.gifRows = _.chunk(allGifs, 4);
            });

        $scope.filter = function() {
            var regex = new RegExp($scope.search, 'gi');

            if ($scope.search.length === 0) {
                $scope.gifRows = _.chunk(allGifs, 4);
                return;
            }

            $scope.gifRows = _.chunk(_.filter(allGifs, function(gif) {
                return regex.test(gif.title) || regex.test(gif.tags.join(' '));
            }), 4);
        };

        function getWebmUrl(gfycat) {
            return 'http://zippy.gfycat.com/' + gfycat + '.webm';
        }

        function getMp4Url(gfycat) {
            return 'http://zippy.gfycat.com/' + gfycat + '.mp4';
        }
    }]);
})();
