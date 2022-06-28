import asana

client_asana = asana.Client.access_token("1/383667085808411:fe9ad11908a3bae3f063662649f7e589")


def get_workspace_map(workspace_name):
    """
    Создание "КАРТЫ" рабочего пространства, определение gid воркспэйса по имени
    Возвращает кортеж вида ("workspace_gid", workspace_map ),
    где workspace_map это словарь вида:
     {
     ("project_name", "project_gid"): [{"gid": "gid_task_1", "name": "name_task_1"},
                                         {"gid": "gid_task_2", "name": "name_task_2"},
                                         ......
                                         {"gid": "gid_task_N", "name": "name_task_N"}]
     }
    """
    result_project_dict = {}

    results_workspaces = client_asana.workspaces.get_workspaces(opt_pretty=True)

    for result_workspaces in results_workspaces:

        if result_workspaces["name"] == workspace_name:
            result_projects = client_asana.projects.get_projects({"workspace": result_workspaces["gid"]},
                                                                 opt_pretty=True)
            for project in result_projects:
                result_tasks = client_asana.tasks.get_tasks({"project": project["gid"]}, opt_pretty=True)
                result_project_dict[(project["name"], project["gid"])] = list(result_tasks)

            return result_workspaces["gid"], result_project_dict


def get_gid_project(workspace_name, project_name):
    """ Поиск gid проекта Сборка """

    _, workspace_map = get_workspace_map(workspace_name)

    assembly_project_list = []
    for name, gid in workspace_map:
        if name == project_name:
            assembly_project_list.append(gid)
    if len(assembly_project_list) == 1:
        return assembly_project_list[0]
    elif len(assembly_project_list) > 1:
        raise ValueError(f"\n\n  ---> Обнаружено несколько проектов с названием '{project_name}' !!!\n")
    elif len(assembly_project_list) < 1:
        raise ValueError(f"\n\n  ---> Проектов с названием '{project_name}' не обнаружено!!!\n")


def get_user_gid(workspace_gid, user_name):
    """ Поиск gid проекта Сборка """

    results = client_asana.users.get_users({"workspace": workspace_gid}, opt_pretty=True)
    result_list = [result for result in results if result["name"] == user_name]

    return result_list[0] if len(result_list) == 1 else None
