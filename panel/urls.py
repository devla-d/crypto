from django.urls import path
from .import views
from .views import PackagesDeleteView,PackageUpdateView
from django.conf.urls import handler404, handler500


urlpatterns = [
    path('admin/', views.dashboard, name="dashboard"),
    path('admin/login/', views.login_view, name="dashboard-login"),
    path('admin/logout/', views.logout_view, name="dashboard-logout"),
    path('admin/users/', views.users, name="users"),
    path('admin/message/', views.message, name="message"),
    path('admin/notify-user/', views.notify_user, name="notify-user"),
    path('admin/package/new', views.new_package, name="new_package"),
    path('package/<int:pk>/update/', PackageUpdateView.as_view(), name='package-update'),
    path('package/<int:pk>/delete/', PackagesDeleteView.as_view(), name='package-delete'),

    path('admin/users/<str:ref_code>/detail/', views.users_detail, name="users-detail"),
    path('admin/users/enable/', views.enable_profile, name="enable_profile"),
    path('admin/users/disable/', views.disable_profile, name="disable_profile"),
    path('admin/users/add_fund/', views.add_funds, name="add_funds"),
    path('admin/users/deduct/', views.deduct_funds, name="deduct_funds"),
    path('admin/withdraws/', views.withdrws, name="admin-withdraw"),
    path('admin/transaction/', views.transaction, name="admin-transaction"),
    path('admin/deposite/', views.deposite, name="admin-deposite"),
    path('admin/package/', views.package, name="admin-package"),
    path('admin/withdraw/pay/', views.pay_users, name="deduct_funds"),
    path('admin/withdraw/decline/', views.decline_pay_users, name="decline_pay_users"),
    path('admin/withdraws/<int:pk>', views.withdrws_deteail, name="admin-withdraw-detail"),
    path('admin/deposite/<int:pk>', views.deposite_deteail, name="admin-deposite-deteail"),
    path('admin/deposite/accept/', views.accept_deposite, name="accept_deposite"),
    path('admin/deposite/decline/', views.decline_deposite, name="decline_deposite"),

]


"""handler404 = views.error_404
handler500 = views.error_500"""