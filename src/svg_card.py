def generate(stats, template, config):
    tmp = ""
    lang_count = len(stats["top_lang"])
    del_lang_other = False
    percent_lang_other = 0
    if lang_count < 11:
        del_lang_other = True
        lang = stats["top_lang"]
        for i in range(10 - lang_count):
            lang.append(None)
    else:
        lang = stats["top_lang"][:10]
        for i in stats["top_lang"][10:]:
            percent_lang_other += i[2]
    for line in template.split("\n"):
        add_line = True
        _  = line.split(" ")
        for f in _:
            if f == f"id=\"{config['total_stars_earned'][0]}\"":
                tmp += line.replace(config['total_stars_earned'][1], str(stats["total_stars_earned"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['total_commits'][0]}\"":
                tmp += line.replace(config['total_commits'][1], str(stats["total_commits"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['total_issues'][0]}\"":
                tmp += line.replace(config['total_issues'][1], str(stats["total_issues"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['total_forks_earned'][0]}\"":
                tmp += line.replace(config['total_forks_earned'][1], str(stats["total_forks_earned"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['total_repos'][0]}\"":
                tmp += line.replace(config['total_repos'][1], str(stats["total_repos"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['total_forks_repos'][0]}\"":
                tmp += line.replace(config['total_forks_repos'][1], str(stats["total_forks_repos"])) + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['pull_request'][0]}\"":
                tmp1 = line.replace(config['pull_request'][1], str(stats["pull_request"]["open"]))
                tmp1 = tmp1.replace(config['pull_request'][2], str(stats["pull_request"]["merged"]))
                tmp1 = tmp1.replace(config['pull_request'][3], str(stats["pull_request"]["closed"]))
                tmp += tmp1 + "\n"
                add_line = False
                break
            elif f == f"id=\"{config['lang_other'][0]}\"":
                add_line = False
                if del_lang_other:
                    break
                else:
                    tmp += line.replace(config['lang_other'][1], "{:.2f}".format(percent_lang_other)) + "\n"
            elif (f == f"id=\"{config['lang_other'][2]}\"" or f == f"id=\"{config['lang_other'][3]}\"") and del_lang_other:
                add_line = False
                break
            else:
                for l in range(1, 11):
                    if f == f"id=\"{config['lang_' + str(l)][0]}\"":
                        if lang[l - 1] != None:
                            tmp1 = line.replace(config['lang_' + str(l)][1], str(lang[l - 1][0]))
                            tmp1 = tmp1.replace(config['lang_' + str(l)][2], "{:.2f}".format(lang[l - 1][2]))
                            tmp += tmp1 + "\n"
                        add_line = False
                        break
                    elif f == f"id=\"{config['lang_' + str(l)][3]}\"":
                        if lang[l - 1] != None:
                            tmp += line.replace("#000000", stats["lang_stats"][lang[l - 1][0]]["color"]) + "\n"
                        add_line = False
                        break
                    elif f == f"id=\"{config['lang_' + str(l)][4]}\"":
                        if lang[l - 1] != None:
                            tmp1 = line.replace("#000000", stats["lang_stats"][lang[l - 1][0]]["color"])
                            tmp2 = 0
                            for i in range(l):
                                tmp2 += lang[i][2]
                            tmp1 = tmp1.replace(f"\"{config['line_width_max']}\"", "\"" + ("{:.5f}".format((tmp2 / 100) * float(config['line_width_max']))) + "\"")
                            tmp += tmp1 + "\n"
                        add_line = False
                        break
        if add_line:
            tmp += line + "\n"
    return tmp

if __name__ == "__main__":
    import json
    config = json.loads(open("template.json", "r", encoding="utf-8").read())
    stats = json.loads(open("tmp/stats", "r", encoding="utf-8").read())
    template = open("template.svg", "r", encoding="utf-8").read()
    template_l = template
    template_d = template
    for r in config["dark2light"]:
        template_l = template_l.replace(r[0], r[1])
    template_l = generate(stats, template_l, config)
    template_d = generate(stats, template_d, config)
    open("tmp/stats_light.svg", "w", encoding="utf-8").write(template_l)
    open("tmp/stats_dark.svg", "w", encoding="utf-8").write(template_d)

