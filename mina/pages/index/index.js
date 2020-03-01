//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag: true
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/food/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    });
    // this.login();
    this.checkLogin();
  },
  onShow:function(){

  },
  onReady: function(){
    var that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
  checkLogin: function () {
    var that = this;
    wx.login({
      success:function(res) {
        if (res.code) {
          //发起网络请求
          wx.request({
              url: app.buildUrl('/member/check-reg'),
              method: 'POST',
              header: app.getRequestHeader(),
              data: {code: res.code},
              success: function (res) {
                if(res.data.code != 200){
                  that.setData({
                      regFlag: false
                  });
                  return;
                }
                app.setCache("token", res.data.data.token);
                // that.goToIndex();
              }
          })
        } else {
          app.alert('登录失败！' + res.errMsg);
          return;
        }
      }
    })
  },
  login: function (e) {
    var that = this;
    var data = e.detail.userInfo;
    if(!e.detail.userInfo){
      app.alert({'content': '登录失败，请再次点击~'});
      return;
    }
    wx.login({
      success:function(res) {
        if (res.code) {
          data['code'] = res.code;
          //发起网络请求
          wx.request({
              url: app.buildUrl('/member/login'),
              method: 'POST',
              header: app.getRequestHeader(),
              data: data,
              success: function (res) {
                if(res.data.code != 200){
                  app.alert({'content': res.data.msg});
                  return;
                }
                app.setCache("token", res.data.data.token);
                // that.goToIndex();
              }
          })
        } else {
          app.alert('登录失败！' + res.errMsg)
        }
      }
    })
  }
});