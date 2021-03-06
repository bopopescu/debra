# -*- coding: utf-8 -*- #
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Delete network endpoint groups command."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.network_endpoint_groups import flags
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


class Delete(base.DeleteCommand):
  """Deletes a Google Compute Engine network endpoint group."""

  @staticmethod
  def Args(parser):
    flags.MakeNetworkEndpointGroupsArg().AddArgument(parser)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    neg_ref = flags.MakeNetworkEndpointGroupsArg().ResolveAsResource(
        args, holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(holder.client))
    console_io.PromptContinue(
        'You are about to delete network endpoint group: [{}]'.format(
            neg_ref.Name()),
        throw_if_unattended=True, cancel_on_no=True)

    messages = holder.client.messages
    request = messages.ComputeNetworkEndpointGroupsDeleteRequest(
        networkEndpointGroup=neg_ref.Name(),
        project=neg_ref.project,
        zone=neg_ref.zone)

    service = holder.client.apitools_client.networkEndpointGroups
    result = client.MakeRequests([(service, 'Delete', request)])
    log.DeletedResource(neg_ref.Name(), 'network endpoint group')
    return result
