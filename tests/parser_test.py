from parser_engine.parser import PEParser


def test_cast():
    p = PEParser()
    v = p.cast(["daj"], 'singleton')
    assert v == "daj"


def test_parse_text():
    s = '''{"result":"success","msg":"成功","data":[{"id":"111073566","uniqueId":"10.10.59.240-1551756361.37683","numberTrunk":"02160662484","customerNumber":"17717033871","encryptCustomerNumber":"17717033871","customerNumberType":null,"customerAreaCode":null,"customerProvince":"上海","customerCity":"上海","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"17","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"183","sipCauseDesc":"彩铃","startTimeString":"2019-03-05 11:26:01","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:17","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"111066777","uniqueId":"10.10.59.240-1551756246.37127","numberTrunk":"02160662489","customerNumber":"17318549829","encryptCustomerNumber":"17318549829","customerNumberType":null,"customerAreaCode":null,"customerProvince":"安徽","customerCity":"合肥","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"0","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"0","sipCauseDesc":"","startTimeString":"2019-03-05 11:24:06","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:00","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"111068756","uniqueId":"10.10.59.240-1551756243.37114","numberTrunk":"02160662489","customerNumber":"17318549829","encryptCustomerNumber":"17318549829","customerNumberType":null,"customerAreaCode":null,"customerProvince":"安徽","customerCity":"合肥","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"42","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"480","sipCauseDesc":"未接通","startTimeString":"2019-03-05 11:24:03","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:42","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"110301141","uniqueId":"10.10.59.240-1551689999.107468","numberTrunk":"02160662487","customerNumber":"010345678","encryptCustomerNumber":"010345678","customerNumberType":null,"customerAreaCode":null,"customerProvince":"北京","customerCity":"北京","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"34","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"0301","userField":"","sipCause":"480","sipCauseDesc":"未接通","startTimeString":"2019-03-04 16:59:59","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:34","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"预览外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"110293692","uniqueId":"10.10.59.240-1551689848.106818","numberTrunk":"02160662484","customerNumber":"18692709883","encryptCustomerNumber":"18692709883","customerNumberType":null,"customerAreaCode":null,"customerProvince":"湖南","customerCity":"益阳","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"33","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"0301","userField":"","sipCause":"480","sipCauseDesc":"未接通","startTimeString":"2019-03-04 16:57:28","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:33","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"预览外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"110167223","uniqueId":"10.10.59.240-1551687431.95576","numberTrunk":"02160662487","customerNumber":"13807802330","encryptCustomerNumber":"13807802330","customerNumberType":null,"customerAreaCode":null,"customerProvince":"广西","customerCity":"南宁|崇左","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"26","cost":"0.070","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"21","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"0304-1","userField":"","sipCause":"200","sipCauseDesc":"处理成功","startTimeString":"2019-03-04 16:17:11","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:26","statusString":"客户未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"预览外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"109709284","uniqueId":"10.10.59.240-1551678317.54294","numberTrunk":"02160662484","customerNumber":"010333333","encryptCustomerNumber":"010333333","customerNumberType":null,"customerAreaCode":null,"customerProvince":"北京","customerCity":"北京","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"45","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"0304","userField":"","sipCause":"183","sipCauseDesc":"彩铃","startTimeString":"2019-03-04 13:45:17","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:45","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"预览外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"106672035","uniqueId":"10.10.59.240-1551427681.94179","numberTrunk":"02160662484","customerNumber":"010345678","encryptCustomerNumber":"010345678","customerNumberType":null,"customerAreaCode":null,"customerProvince":"北京","customerCity":"北京","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"45","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"183","sipCauseDesc":"彩铃","startTimeString":"2019-03-01 16:08:01","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:45","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"106669083","uniqueId":"10.10.59.240-1551427617.93881","numberTrunk":"02160662487","customerNumber":"010345678","encryptCustomerNumber":"010345678","customerNumberType":null,"customerAreaCode":null,"customerProvince":"北京","customerCity":"北京","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"46","cost":"0.000","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"24","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"183","sipCauseDesc":"彩铃","startTimeString":"2019-03-01 16:06:56","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:46","statusString":"座席未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null},{"id":"106634842","uniqueId":"10.10.59.240-1551426911.90880","numberTrunk":"02160662487","customerNumber":"010345678","encryptCustomerNumber":"010345678","customerNumberType":null,"customerAreaCode":null,"customerProvince":"北京","customerCity":"北京","customerCrmId":null,"clientNumber":"18964998287","clientAreaCode":null,"cno":"2000","exten":null,"clientName":"2000","clientCrmId":null,"startTime":null,"answerTime":null,"bridgeTime":null,"endTime":null,"billDuration":"0","bridgeDuration":"0","totalDuration":"32","cost":"0.070","totalCost":null,"comboCost":"0","ivrId":null,"ivrName":"","queueName":"","recordFile":"","score":"0","scoreComment":"","inCaseLib":"0","callType":null,"status":"22","mark":"0","markData":"","endReason":"0","gwIp":null,"createTime":"1551930051190","taskId":null,"taskName":"","userField":"","sipCause":"200","sipCauseDesc":"处理成功","startTimeString":"2019-03-01 15:55:11","bridgeTimeString":"-","bridgeDurationString":"00:00:00","totalDurationString":"00:00:32","statusString":"客户未接听","inCaseLibString":"不在","comment":"无","endReasonString":"否","callTypeString":"点击外呼","hotline":null,"obLeftDuration":null,"obRightDuration":null,"asrDuration":null,"asrCost":null,"recordFileName":null,"userName":null,"virtualNumber":"","sqcCost":null,"dualRecordCost":null}]}
'''
    tpl_s = {
        "name": "tian_cdrOb",
        "itemname": "CallRecordItem",
        "parent": {
            "json_key": "data"
        },
        "fields": [
            {
                "description": "客户电话",
                "key": "customer_number",
                "json_key": "customerNumber"
            },
            {
                "description": "中继号码",
                "json_key": ""
            },
            {
                "description": "座席工号",
                "json_key": "cno",
                "key": "work_number"
            },
            {
                "description": "座席姓名",
                "json_key": ""
            },
            {
                "description": "座席电话",
                "json_key": ""
            },
            {
                "description": "虚拟号码",
                "json_key": ""
            },
            {
                "description": "开始时间",
                "json_key": ""
            },
            {
                "description": "接听时间",
                "json_key": ""
            },
            {
                "description": "接听状态",
                "json_key": ""
            },
            {
                "description": "通话时长",
                "json_key": ""
            },
            {
                "description": "套餐分钟数",
                "json_key": ""
            },
            {
                "description": "话费（元）",
                "json_key": ""
            },
            {
                "description": "总时长",
                "json_key": ""
            },
            {
                "description": "呼叫类型",
                "json_key": ""
            },
            {
                "description": "外呼任务",
                "json_key": ""
            },
            {
                "description": "录音",
                "json_key": ""
            },
            {
                "description": "备注",
                "json_key": ""
            },
            {
                "description": "客户挂机",
                "json_key": ""
            },
            {
                "description": "呼叫情况",
                "json_key": ""
            },
            {
                "description": "转写计费时长（分）",
                "json_key": ""
            },
            {
                "description": "双轨录音费用（元）",
                "json_key": ""
            },
            {
                "description": "转写费用（元）",
                "json_key": ""
            },
            {
                "description": "智能质检费用（元）",
                "json_key": ""
            },
            {
                "description": "唯一标识",
                "json_key": ""
            },
            {
                "description": "座席电话",
                "json_key": ""
            },
            {
                "description": "虚拟号码",
                "json_key": ""
            }
        ]
    }
    items = PEParser(tpl=tpl_s, lazy_load=True)._parse_text(s)
    print(items)


def parse_text_xpath():
    tpl = {"name": "customerUpdate",
           "itemname": 'CustomerItem',
           "fields": [{
               "key": "name",
               "tags": ["td", "input"],
               "attributes": "alt=\"姓名\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "outbound_time",
               "tags": ["td", "input"],
               "attributes": "alt=\"出库时间\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "mobile1",
               "tags": ["td", "input"],
               "attributes": "alt=\"\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "wechat",
               "tags": ["td", "input"],
               "attributes": "alt=\"微信号\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "nickname",
               "tags": ["td", "input"],
               "attributes": "alt=\"昵称\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "qualified_company_name",
               "tags": ["td", "input"],
               "attributes": "alt=\"认证公司名称\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "first_category",
               "tags": ["td", "input"],
               "attributes": "alt=\"一级类目\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "second_category",
               "tags": ["td", "input"],
               "attributes": "alt=\"二级类目\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "city",
               "tags": ["td", "input"],
               "attributes": "alt=\"所在城市\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "leads_src",
               "__xpath": "//td//select[@alt=\"线索来源\"]/option[@selected and @value != '']/text()",
               "value_type": "singleton"
           }, {
               "key": "douyin_mobile",
               "tags": ["td", "input"],
               "attributes": "alt=\"注册抖音手机\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "douyin_nickname",
               "tags": ["td", "input"],
               "attributes": "alt=\"抖音用户昵称\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "douyin_id",
               "tags": ["td", "input"],
               "attributes": "alt=\"抖音ID号\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "company_name",
               "tags": ["td", "input"],
               "attributes": "alt=\"公司名称\"",
               "attr_name": "value",
               "value_type": "singleton"
           }, {
               "key": "create_time",
               "tags": ["td", "input"],
               "attributes": "alt=\"创建时间\"",
               "attr_name": "value",
               "value_type": "singleton"
           }]
           }
    PEParser(tpl).parse_html(None)


if __name__ == '__main__':
    test_parse_text()
