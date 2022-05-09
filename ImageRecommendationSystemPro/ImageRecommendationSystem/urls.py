import sys
sys.path.append('../views/')
import os
from . import views#导入所需的视图函数
from django.conf.urls import url,include
from django.urls import path,re_path 
from django.views.static import serve
from ImageRecommendationSystemPro.settings import *

urlpatterns = [
	url('error/',views.PublicView.my_decorator(views.PublicView.ErrorInfo.as_view())), 
	url('error/authorrityError/',views.PublicView.ErrorInfo.showErroInfo,name="showerroinfo"),

 
    url('admin/SystemAccount/',views.PublicView.my_decorator(views.SystemAccountView.SystemAccount.as_view())),
    url('admin/SystemAccount/add/',views.SystemAccountView.SystemAccount.add,name="systemaccountadd"),
    url('admin/SystemAccount/index/',views.SystemAccountView.SystemAccount.index,name="systemaccountindex"),
    url('admin/SystemAccount/save_add/',views.SystemAccountView.SystemAccount.save_add,name="systemaccountsaveadd"),
    url('admin/SystemAccount/edit/',views.SystemAccountView.SystemAccount.edit,name="systemaccountedit"),
    url('admin/SystemAccount/save_edit/',views.SystemAccountView.SystemAccount.save_edit,name="systemaccountsaveedit"),   
    url('admin/SystemAccount/delete/',views.SystemAccountView.SystemAccount.delete,name="systemaccountdelete"),
    url('admin/SystemAccount/delete_all/',views.SystemAccountView.SystemAccount.delete_all,name="systemaccountdeleteall"),
    url('admin/SystemAccount/playvedio/',views.SystemAccountView.SystemAccount.playvedio,name="systemaccountplayvedio"),
    url('admin/SystemAccount/detail/',views.SystemAccountView.SystemAccount.detail,name="systemaccountdetail"),
    url('admin/SystemAccount/import_excel/',views.SystemAccountView.SystemAccount.import_excel,name="systemaccountimportexcel"),   
    url('admin/SystemAccount/export_excel/',views.SystemAccountView.SystemAccount.export_excel,name="systemaccountexportexcel"), 
    url('admin/SystemAccount/download_excel/',views.SystemAccountView.SystemAccount.download_excel,name="systemaccountdownloadexcel"), 
    url('admin/SystemAccount/getInfo/',views.SystemAccountView.SystemAccount.getInfo,name="systemaccountgetinfo"),
         
     
    url('admin/Member/',views.PublicView.my_decorator(views.MemberView.Member.as_view())),
    url('admin/Member/add/',views.MemberView.Member.add,name="memberadd"),
    url('admin/Member/index/',views.MemberView.Member.index,name="memberindex"),
    url('admin/Member/save_add/',views.MemberView.Member.save_add,name="membersaveadd"),
    url('admin/Member/edit/',views.MemberView.Member.edit,name="memberedit"),
    url('admin/Member/save_edit/',views.MemberView.Member.save_edit,name="membersaveedit"),   
    url('admin/Member/delete/',views.MemberView.Member.delete,name="memberdelete"),
    url('admin/Member/delete_all/',views.MemberView.Member.delete_all,name="memberdeleteall"),
    url('admin/Member/playvedio/',views.MemberView.Member.playvedio,name="memberplayvedio"),
    url('admin/Member/detail/',views.MemberView.Member.detail,name="memberdetail"),
    url('admin/Member/import_excel/',views.MemberView.Member.import_excel,name="memberimportexcel"),   
    url('admin/Member/export_excel/',views.MemberView.Member.export_excel,name="memberexportexcel"), 
    url('admin/Member/download_excel/',views.MemberView.Member.download_excel,name="memberdownloadexcel"), 
    url('admin/Member/getInfo/',views.MemberView.Member.getInfo,name="membergetinfo"),
         
     
    url('admin/ImageType/',views.PublicView.my_decorator(views.ImageTypeView.ImageType.as_view())),
    url('admin/ImageType/add/',views.ImageTypeView.ImageType.add,name="imagetypeadd"),
    url('admin/ImageType/index/',views.ImageTypeView.ImageType.index,name="imagetypeindex"),
    url('admin/ImageType/save_add/',views.ImageTypeView.ImageType.save_add,name="imagetypesaveadd"),
    url('admin/ImageType/edit/',views.ImageTypeView.ImageType.edit,name="imagetypeedit"),
    url('admin/ImageType/save_edit/',views.ImageTypeView.ImageType.save_edit,name="imagetypesaveedit"),   
    url('admin/ImageType/delete/',views.ImageTypeView.ImageType.delete,name="imagetypedelete"),
    url('admin/ImageType/delete_all/',views.ImageTypeView.ImageType.delete_all,name="imagetypedeleteall"),
    url('admin/ImageType/playvedio/',views.ImageTypeView.ImageType.playvedio,name="imagetypeplayvedio"),
    url('admin/ImageType/detail/',views.ImageTypeView.ImageType.detail,name="imagetypedetail"),
    url('admin/ImageType/import_excel/',views.ImageTypeView.ImageType.import_excel,name="imagetypeimportexcel"),   
    url('admin/ImageType/export_excel/',views.ImageTypeView.ImageType.export_excel,name="imagetypeexportexcel"), 
    url('admin/ImageType/download_excel/',views.ImageTypeView.ImageType.download_excel,name="imagetypedownloadexcel"), 
    url('admin/ImageType/getInfo/',views.ImageTypeView.ImageType.getInfo,name="imagetypegetinfo"),
         
     
    url('admin/ImageInformation/',views.PublicView.my_decorator(views.ImageInformationView.ImageInformation.as_view())),
    url('admin/ImageInformation/add/',views.ImageInformationView.ImageInformation.add,name="imageinformationadd"),
    url('admin/ImageInformation/index/',views.ImageInformationView.ImageInformation.index,name="imageinformationindex"),
    url('admin/ImageInformation/save_add/',views.ImageInformationView.ImageInformation.save_add,name="imageinformationsaveadd"),
    url('admin/ImageInformation/edit/',views.ImageInformationView.ImageInformation.edit,name="imageinformationedit"),
    url('admin/ImageInformation/save_edit/',views.ImageInformationView.ImageInformation.save_edit,name="imageinformationsaveedit"),   
    url('admin/ImageInformation/delete/',views.ImageInformationView.ImageInformation.delete,name="imageinformationdelete"),
    url('admin/ImageInformation/delete_all/',views.ImageInformationView.ImageInformation.delete_all,name="imageinformationdeleteall"),
    url('admin/ImageInformation/playvedio/',views.ImageInformationView.ImageInformation.playvedio,name="imageinformationplayvedio"),
    url('admin/ImageInformation/detail/',views.ImageInformationView.ImageInformation.detail,name="imageinformationdetail"),
    url('admin/ImageInformation/import_excel/',views.ImageInformationView.ImageInformation.import_excel,name="imageinformationimportexcel"),   
    url('admin/ImageInformation/export_excel/',views.ImageInformationView.ImageInformation.export_excel,name="imageinformationexportexcel"), 
    url('admin/ImageInformation/download_excel/',views.ImageInformationView.ImageInformation.download_excel,name="imageinformationdownloadexcel"), 
    url('admin/ImageInformation/getInfo/',views.ImageInformationView.ImageInformation.getInfo,name="imageinformationgetinfo"),
    
    url('admin/ImageInformation/ImageInformationAction/',views.ImageInformationView.ImageInformation.ImageInformationAction,name="imageinformationaction"), 
    url('admin/ImageInformation/ImageInformationAddComment/',views.ImageInformationView.ImageInformation.ImageInformationAddComment,name="imageinformationaddcomment"),
    url('admin/ImageInformation/keywordSearch/',views.ImageInformationView.ImageInformation.keywordSearch,name="imageinformationkeywordsearch"),
               
     
    url('admin/ImageTags/',views.PublicView.my_decorator(views.ImageTagsView.ImageTags.as_view())),
    url('admin/ImageTags/add/',views.ImageTagsView.ImageTags.add,name="imagetagsadd"),
    url('admin/ImageTags/index/',views.ImageTagsView.ImageTags.index,name="imagetagsindex"),
    url('admin/ImageTags/save_add/',views.ImageTagsView.ImageTags.save_add,name="imagetagssaveadd"),
    url('admin/ImageTags/edit/',views.ImageTagsView.ImageTags.edit,name="imagetagsedit"),
    url('admin/ImageTags/save_edit/',views.ImageTagsView.ImageTags.save_edit,name="imagetagssaveedit"),   
    url('admin/ImageTags/delete/',views.ImageTagsView.ImageTags.delete,name="imagetagsdelete"),
    url('admin/ImageTags/delete_all/',views.ImageTagsView.ImageTags.delete_all,name="imagetagsdeleteall"),
    url('admin/ImageTags/playvedio/',views.ImageTagsView.ImageTags.playvedio,name="imagetagsplayvedio"),
    url('admin/ImageTags/detail/',views.ImageTagsView.ImageTags.detail,name="imagetagsdetail"),
    url('admin/ImageTags/import_excel/',views.ImageTagsView.ImageTags.import_excel,name="imagetagsimportexcel"),   
    url('admin/ImageTags/export_excel/',views.ImageTagsView.ImageTags.export_excel,name="imagetagsexportexcel"), 
    url('admin/ImageTags/download_excel/',views.ImageTagsView.ImageTags.download_excel,name="imagetagsdownloadexcel"), 
    url('admin/ImageTags/getInfo/',views.ImageTagsView.ImageTags.getInfo,name="imagetagsgetinfo"),
         
     
    url('admin/FocusOn/',views.PublicView.my_decorator(views.FocusOnView.FocusOn.as_view())),
    url('admin/FocusOn/add/',views.FocusOnView.FocusOn.add,name="focusonadd"),
    url('admin/FocusOn/index/',views.FocusOnView.FocusOn.index,name="focusonindex"),
    url('admin/FocusOn/save_add/',views.FocusOnView.FocusOn.save_add,name="focusonsaveadd"),
    url('admin/FocusOn/edit/',views.FocusOnView.FocusOn.edit,name="focusonedit"),
    url('admin/FocusOn/save_edit/',views.FocusOnView.FocusOn.save_edit,name="focusonsaveedit"),   
    url('admin/FocusOn/delete/',views.FocusOnView.FocusOn.delete,name="focusondelete"),
    url('admin/FocusOn/delete_all/',views.FocusOnView.FocusOn.delete_all,name="focusondeleteall"),
    url('admin/FocusOn/playvedio/',views.FocusOnView.FocusOn.playvedio,name="focusonplayvedio"),
    url('admin/FocusOn/detail/',views.FocusOnView.FocusOn.detail,name="focusondetail"),
    url('admin/FocusOn/import_excel/',views.FocusOnView.FocusOn.import_excel,name="focusonimportexcel"),   
    url('admin/FocusOn/export_excel/',views.FocusOnView.FocusOn.export_excel,name="focusonexportexcel"), 
    url('admin/FocusOn/download_excel/',views.FocusOnView.FocusOn.download_excel,name="focusondownloadexcel"), 
    url('admin/FocusOn/getInfo/',views.FocusOnView.FocusOn.getInfo,name="focusongetinfo"),
         
     
    url('admin/Comment/',views.PublicView.my_decorator(views.CommentView.Comment.as_view())),
    url('admin/Comment/add/',views.CommentView.Comment.add,name="commentadd"),
    url('admin/Comment/index/',views.CommentView.Comment.index,name="commentindex"),
    url('admin/Comment/save_add/',views.CommentView.Comment.save_add,name="commentsaveadd"),
    url('admin/Comment/edit/',views.CommentView.Comment.edit,name="commentedit"),
    url('admin/Comment/save_edit/',views.CommentView.Comment.save_edit,name="commentsaveedit"),   
    url('admin/Comment/delete/',views.CommentView.Comment.delete,name="commentdelete"),
    url('admin/Comment/delete_all/',views.CommentView.Comment.delete_all,name="commentdeleteall"),
    url('admin/Comment/playvedio/',views.CommentView.Comment.playvedio,name="commentplayvedio"),
    url('admin/Comment/detail/',views.CommentView.Comment.detail,name="commentdetail"),
    url('admin/Comment/import_excel/',views.CommentView.Comment.import_excel,name="commentimportexcel"),   
    url('admin/Comment/export_excel/',views.CommentView.Comment.export_excel,name="commentexportexcel"), 
    url('admin/Comment/download_excel/',views.CommentView.Comment.download_excel,name="commentdownloadexcel"), 
    url('admin/Comment/getInfo/',views.CommentView.Comment.getInfo,name="commentgetinfo"),
         
     
    url('admin/Likes/',views.PublicView.my_decorator(views.LikesView.Likes.as_view())),
    url('admin/Likes/add/',views.LikesView.Likes.add,name="likesadd"),
    url('admin/Likes/index/',views.LikesView.Likes.index,name="likesindex"),
    url('admin/Likes/save_add/',views.LikesView.Likes.save_add,name="likessaveadd"),
    url('admin/Likes/edit/',views.LikesView.Likes.edit,name="likesedit"),
    url('admin/Likes/save_edit/',views.LikesView.Likes.save_edit,name="likessaveedit"),   
    url('admin/Likes/delete/',views.LikesView.Likes.delete,name="likesdelete"),
    url('admin/Likes/delete_all/',views.LikesView.Likes.delete_all,name="likesdeleteall"),
    url('admin/Likes/playvedio/',views.LikesView.Likes.playvedio,name="likesplayvedio"),
    url('admin/Likes/detail/',views.LikesView.Likes.detail,name="likesdetail"),
    url('admin/Likes/import_excel/',views.LikesView.Likes.import_excel,name="likesimportexcel"),   
    url('admin/Likes/export_excel/',views.LikesView.Likes.export_excel,name="likesexportexcel"), 
    url('admin/Likes/download_excel/',views.LikesView.Likes.download_excel,name="likesdownloadexcel"), 
    url('admin/Likes/getInfo/',views.LikesView.Likes.getInfo,name="likesgetinfo"),
         
     
    url('admin/SearchHistory/',views.PublicView.my_decorator(views.SearchHistoryView.SearchHistory.as_view())),
    url('admin/SearchHistory/add/',views.SearchHistoryView.SearchHistory.add,name="searchhistoryadd"),
    url('admin/SearchHistory/index/',views.SearchHistoryView.SearchHistory.index,name="searchhistoryindex"),
    url('admin/SearchHistory/save_add/',views.SearchHistoryView.SearchHistory.save_add,name="searchhistorysaveadd"),
    url('admin/SearchHistory/edit/',views.SearchHistoryView.SearchHistory.edit,name="searchhistoryedit"),
    url('admin/SearchHistory/save_edit/',views.SearchHistoryView.SearchHistory.save_edit,name="searchhistorysaveedit"),   
    url('admin/SearchHistory/delete/',views.SearchHistoryView.SearchHistory.delete,name="searchhistorydelete"),
    url('admin/SearchHistory/delete_all/',views.SearchHistoryView.SearchHistory.delete_all,name="searchhistorydeleteall"),
    url('admin/SearchHistory/playvedio/',views.SearchHistoryView.SearchHistory.playvedio,name="searchhistoryplayvedio"),
    url('admin/SearchHistory/detail/',views.SearchHistoryView.SearchHistory.detail,name="searchhistorydetail"),
    url('admin/SearchHistory/import_excel/',views.SearchHistoryView.SearchHistory.import_excel,name="searchhistoryimportexcel"),   
    url('admin/SearchHistory/export_excel/',views.SearchHistoryView.SearchHistory.export_excel,name="searchhistoryexportexcel"), 
    url('admin/SearchHistory/download_excel/',views.SearchHistoryView.SearchHistory.download_excel,name="searchhistorydownloadexcel"), 
    url('admin/SearchHistory/getInfo/',views.SearchHistoryView.SearchHistory.getInfo,name="searchhistorygetinfo"),
         
     
    url('admin/BrowsingHistory/',views.PublicView.my_decorator(views.BrowsingHistoryView.BrowsingHistory.as_view())),
    url('admin/BrowsingHistory/add/',views.BrowsingHistoryView.BrowsingHistory.add,name="browsinghistoryadd"),
    url('admin/BrowsingHistory/index/',views.BrowsingHistoryView.BrowsingHistory.index,name="browsinghistoryindex"),
    url('admin/BrowsingHistory/save_add/',views.BrowsingHistoryView.BrowsingHistory.save_add,name="browsinghistorysaveadd"),
    url('admin/BrowsingHistory/edit/',views.BrowsingHistoryView.BrowsingHistory.edit,name="browsinghistoryedit"),
    url('admin/BrowsingHistory/save_edit/',views.BrowsingHistoryView.BrowsingHistory.save_edit,name="browsinghistorysaveedit"),   
    url('admin/BrowsingHistory/delete/',views.BrowsingHistoryView.BrowsingHistory.delete,name="browsinghistorydelete"),
    url('admin/BrowsingHistory/delete_all/',views.BrowsingHistoryView.BrowsingHistory.delete_all,name="browsinghistorydeleteall"),
    url('admin/BrowsingHistory/playvedio/',views.BrowsingHistoryView.BrowsingHistory.playvedio,name="browsinghistoryplayvedio"),
    url('admin/BrowsingHistory/detail/',views.BrowsingHistoryView.BrowsingHistory.detail,name="browsinghistorydetail"),
    url('admin/BrowsingHistory/import_excel/',views.BrowsingHistoryView.BrowsingHistory.import_excel,name="browsinghistoryimportexcel"),   
    url('admin/BrowsingHistory/export_excel/',views.BrowsingHistoryView.BrowsingHistory.export_excel,name="browsinghistoryexportexcel"), 
    url('admin/BrowsingHistory/download_excel/',views.BrowsingHistoryView.BrowsingHistory.download_excel,name="browsinghistorydownloadexcel"), 
    url('admin/BrowsingHistory/getInfo/',views.BrowsingHistoryView.BrowsingHistory.getInfo,name="browsinghistorygetinfo"),
         
     
    url('admin/CommentLikes/',views.PublicView.my_decorator(views.CommentLikesView.CommentLikes.as_view())),
    url('admin/CommentLikes/add/',views.CommentLikesView.CommentLikes.add,name="commentlikesadd"),
    url('admin/CommentLikes/index/',views.CommentLikesView.CommentLikes.index,name="commentlikesindex"),
    url('admin/CommentLikes/save_add/',views.CommentLikesView.CommentLikes.save_add,name="commentlikessaveadd"),
    url('admin/CommentLikes/edit/',views.CommentLikesView.CommentLikes.edit,name="commentlikesedit"),
    url('admin/CommentLikes/save_edit/',views.CommentLikesView.CommentLikes.save_edit,name="commentlikessaveedit"),   
    url('admin/CommentLikes/delete/',views.CommentLikesView.CommentLikes.delete,name="commentlikesdelete"),
    url('admin/CommentLikes/delete_all/',views.CommentLikesView.CommentLikes.delete_all,name="commentlikesdeleteall"),
    url('admin/CommentLikes/playvedio/',views.CommentLikesView.CommentLikes.playvedio,name="commentlikesplayvedio"),
    url('admin/CommentLikes/detail/',views.CommentLikesView.CommentLikes.detail,name="commentlikesdetail"),
    url('admin/CommentLikes/import_excel/',views.CommentLikesView.CommentLikes.import_excel,name="commentlikesimportexcel"),   
    url('admin/CommentLikes/export_excel/',views.CommentLikesView.CommentLikes.export_excel,name="commentlikesexportexcel"), 
    url('admin/CommentLikes/download_excel/',views.CommentLikesView.CommentLikes.download_excel,name="commentlikesdownloadexcel"), 
    url('admin/CommentLikes/getInfo/',views.CommentLikesView.CommentLikes.getInfo,name="commentlikesgetinfo"),
         
    

    url('BrowsingHistoryStatistics/',views.PublicView.my_decorator(views.StatisticsView.BrowsingHistoryStatistics.as_view())),
    url('BrowsingHistoryStatistics/searchData/index/',views.StatisticsView.BrowsingHistoryStatistics.searchData,name='browsinghistorystatisticssearchdata'),   
        
    url('ForegroundDisplayInfo/',views.PublicView.my_decorator(views.ForegroundDisplayInfoView.ForegroundDisplayInfo.as_view())),
        
    url('ForegroundDisplayInfo/ImageInformation_detail/',views.ForegroundDisplayInfoView.ForegroundDisplayInfo.ImageInformation_detail,name='foregrounddisplayinfoimageinformationdetail'),
    
    url('ForegroundDisplayInfo/ImageInformation_listInfo/',views.ForegroundDisplayInfoView.ForegroundDisplayInfo.ImageInformation_listInfo,name='foregrounddisplayinfoimageinformationlistinfo'),
    
    url('ForegroundDisplayInfo/ImageInformation_keywordSearch/',views.ForegroundDisplayInfoView.ForegroundDisplayInfo.ImageInformation_keywordSearch,name='foregrounddisplayinfoimageinformationkeywordsearch'),
    
    url('ForegroundDisplayInfo/ImageInformation_AddComment/',views.ForegroundDisplayInfoView.ForegroundDisplayInfo.ImageInformation_AddComment,name='foregrounddisplayinfoimageinformationaddcomment'),
    
    url('ForegroundDisplayInfo/ImageInformation_Action/',views.ForegroundDisplayInfoView.ForegroundDisplayInfo.ImageInformation_Action,name='foregrounddisplayinfoimageinformationaction'),
    

    url('FrontEnd/',views.PublicView.my_decorator(views.FrontEndView.FrontEnd.as_view())),
    
    url('FrontEnd/Member/add/',views.FrontEndView.FrontEnd.Member_add,name='frontendmemberadd'),
        
    url('FrontEnd/Member/save_add/',views.FrontEndView.FrontEnd.Member_save_add,name='frontendmembersaveadd'),
        
    url('MemberCenter/',views.PublicView.my_decorator(views.MemberCenterView.MemberCenter.as_view())),
    
    url('MemberCenter/Member/edit/',views.MemberCenterView.MemberCenter.Member_edit,name='membercentermemberedit'),
        
    url('MemberCenter/Member/save_edit/',views.MemberCenterView.MemberCenter.Member_save_edit,name='membercentermembersaveedit'),
        
    url('MemberCenter/FocusOn/delete/',views.MemberCenterView.MemberCenter.FocusOn_delete,name='membercenterfocusondelete'),
        
    url('MemberCenter/FocusOn/edit/',views.MemberCenterView.MemberCenter.FocusOn_edit,name='membercenterfocusonedit'),
        
    url('MemberCenter/FocusOn/save_edit/',views.MemberCenterView.MemberCenter.FocusOn_save_edit,name='membercenterfocusonsaveedit'),
        
    url('MemberCenter/FocusOn/search/',views.MemberCenterView.MemberCenter.FocusOn_search,name='membercenterfocusonsearch'),
        
    url('MemberCenter/FocusOn/detail/',views.MemberCenterView.MemberCenter.FocusOn_detail,name='membercenterfocusondetail'),
        
    url('MemberCenter/ImageInformation/add/',views.MemberCenterView.MemberCenter.ImageInformation_add,name='membercenterimageinformationadd'),
        
    url('MemberCenter/ImageInformation/save_add/',views.MemberCenterView.MemberCenter.ImageInformation_save_add,name='membercenterimageinformationsaveadd'),
        
    url('MemberCenter/ImageInformation/delete/',views.MemberCenterView.MemberCenter.ImageInformation_delete,name='membercenterimageinformationdelete'),
        
    url('MemberCenter/ImageInformation/edit/',views.MemberCenterView.MemberCenter.ImageInformation_edit,name='membercenterimageinformationedit'),
        
    url('MemberCenter/ImageInformation/save_edit/',views.MemberCenterView.MemberCenter.ImageInformation_save_edit,name='membercenterimageinformationsaveedit'),
        
    url('MemberCenter/ImageInformation/search/',views.MemberCenterView.MemberCenter.ImageInformation_search,name='membercenterimageinformationsearch'),
        
    url('MemberCenter/ImageInformation/detail/',views.MemberCenterView.MemberCenter.ImageInformation_detail,name='membercenterimageinformationdetail'),
        
    url('MemberCenter/index/',views.MemberCenterView.MemberCenter.index,name='membercenterindex'),
    url('MemberCenter/getPersonInfo/',views.MemberCenterView.MemberCenter.getPersonInfo,name='membercentergetpersoninfo'),


        
    url('MemberCenter/login/',views.MemberCenterView.MemberCenter.login,name='membercenterlogin'),
        
    url('FrontEndIndex/',views.PublicView.my_decorator(views.FrontEndIndexView.FrontEndIndex.as_view())),
    
    url('FrontEndIndex/index/',views.FrontEndIndexView.FrontEndIndex.index,name='frontendindexindex'),
    
    url('FrontEndIndex/logout/',views.FrontEndIndexView.FrontEndIndex.logout,name='frontendindexlogout'),
    
    url('admin/Login/',views.PublicView.my_decorator(views.loginView.Login.as_view())),
    url('admin/Login/index/',views.loginView.Login.index,name="index"),
    url('admin/Login/login/',views.loginView.Login.login,name="login"),
    url('admin/Login/logout/',views.loginView.Login.logout,name="logout"),
    url('admin/Login/register/',views.loginView.Login.register,name="register"), 
            ]