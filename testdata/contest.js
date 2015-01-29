
vr = db.contest.findOne({'contestname':'vr'})
if (!vr) {
	db.contest.insert({
		"contestname" : "vr",
		"organisation" : "tcs",
		"testadmin" : {
			"tadmin1" : {
				"password" : "tadmin1",
				"emaill" : "tadmin1@gmail.com"
			},
			"tadmin2" : {
				"password" : "tadmin2",
				"email" : "tadmin2@gmail.com"
			}
		},
		"testcreator" : {
			"tcreator1" : {
				"password" : "tcreator1"
			},
			"tcreator2" : {
				"password" : "tcreator2"
			}
		},
		"tnc" : "conditions"
	})
}

pvp = db.contest.findOne({'contestname':'pvp'})
if (!pvp) {
	db.contest.insert({
		"contestname" : "pvp",
		"organisation" : "tcs",
		"testadmin" : {
			"tdmin1" : {
				"password" : "tadmin1",
				"emaill" : "tadmin1@gmail.com"
			},
			"tadmin2" : {
				"password" : "tadmin2",
				"email" : "tadmin2@gmail.com"
			}
		},
		"testcreator" : {
			"tcreator1" : {
				"password" : "tcreator1"
			},
			"tcreator2" : {
				"password" : "tcreator2"
			}
		},
		"tnc" : "conditions"
	})
}
